from model.position import Position
from model.person import Person
from dal.person_repo import Person_repo
from dal.position_repo import Position_repo
import xml.etree.ElementTree as ET
from datetime import datetime, date

'''
Author: Jacob Ågård Bennike
Handles the employee aspect of the OPUS XML
'''


class Employee_service:
    def __init__(self, xmlpath, constr_lora):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.constr_lora = constr_lora
        self.persons = {}
        self.positions = {}

    def build_people_and_positions_from_opusxml(self):
        '''
        OPUS XML filen fra KMD indeholder to tags employee og orgunit.
        Denne funktion splitter "employee" tagget op i to dictionaries,
        som indeholder henholdsvis Person og Position objekter, der bliver
        kædet sammen med CPR.
        Der er også en reference til den orgunit som en position tilhører.

        I Person dictionary er CPR nøgle.
        I Position dictionary er OPUS ID (medarbejdernr) nøgle.
        Begge er unikke og ændre sig ikke.

        OBS: Et CPR nr kan i teorien godt ændre sig, hvis en person f.eks.
        skifter køn, men OPUS kan ikke håndtere den slags forandringer, derfor
        er det heller ikke et problem i dette script. Hvis OPUS engang bliver 
        woke, skal scriptet her rettes til.
        '''
        pos_repo = Position_repo(self.constr_lora)
        disabled_orgs = pos_repo.get_disabled_orgunits()
        for emp in self.root.findall('employee'):
            if emp.get('action') == None:
                cpr = emp.find('cpr').text
                opus_id = emp.get('id')
                los_id = int(emp.find('orgUnit').text)
                if los_id in disabled_orgs:
                    # vi har nogle orgunits som indeholder ikke-medarbejdere, dem ønsker vi ikke i SOFD'en og de bliver sorteret fra her.
                    continue

                userId = None
                if emp.find('userId') != None:
                    userId = emp.find('userId').text

                # sætter en start dato fra de forskellige datapunkter vi har at gøre godt med. Det er lidt rodet fordi det er en manuel indtastning fra løn
                # Entry date er aldrig none, men tom når der ikke er en dato
                startdate = None
                if emp.find('entryDate').text != None:
                    startdate = emp.find('entryDate').text
                elif emp.find('initialEntry') != None:
                    startdate = emp.find('initialEntry').text
                elif emp.find('entryIntoGroup') != None:
                    startdate = emp.find('entryIntoGroup').text

                if startdate == None:
                    # Hvis der ikke er en start dato for en stilling, er den oprettet forkert i løn og kan ikke meldes til vores andre systemer, derfor ignorer vi den.
                    print(opus_id)
                    continue
                else:
                    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()

                leavedate = None
                if emp.find('leaveDate') != None:
                    leavedate = emp.find('leaveDate').text

                per = Person(cpr,
                             emp.find('firstName').text,
                             emp.find('lastName').text,
                             emp.find('address').text,
                             emp.find('postalCode').text,
                             emp.find('city').text,
                             emp.find('country').text,
                             True)

                pos = Position(opus_id,
                               None,
                               los_id,
                               cpr,
                               emp.find('cpr').get('suppId'),
                               emp.find('position').text,
                               emp.find('positionId').text,
                               emp.find('positionShort').text,
                               emp.find('payGradeText').text,
                               emp.find('isManager').text,
                               emp.find('workContract').text,
                               emp.find('workContractText').text,
                               emp.find('numerator').text,
                               emp.find('denominator').text,
                               emp.find('invoiceRecipient').text,
                               emp.find('productionNumber').text,
                               userId,
                               startdate,
                               leavedate,
                               None,
                               None,
                               True,
                               False,
                               False)

                self.persons[cpr] = per
                self.positions[int(opus_id)] = pos
            elif emp.get('action') == 'leave':
                # OPUS filen indeholder alle stillinger der har eksisteret, vi sorterer de nedlagte fra her.
                continue

    def get_persons(self):
        return self.persons

    def get_positions(self):
        return self.positions

    def update_persons(self):
        '''
        Funktion der indsætter nye personer fra OPUS, 
        opdaterer personer hvor der er forandringer og sletter 
        personer som ikke længere er en del af vores lønsystem
        '''
        per_repo = Person_repo(self.constr_lora)
        sofd_persons = per_repo.get_persons()
        opus_persons = self.get_persons()
        persons_to_insert = {}
        persons_to_update = {}

        # key er cpr
        for key in opus_persons:
            opus_per = opus_persons[key]
            # hvis personen findes, tjekkes den for forandringer
            if key in sofd_persons:
                sofd_per = sofd_persons[key]
                if opus_per.firstname == sofd_per.firstname and opus_per.lastname == sofd_per.lastname and opus_per.address == sofd_per.address \
                        and opus_per.zipcode == sofd_per.zipcode and opus_per.city == sofd_per.city and opus_per.country == sofd_per.country:
                    # Når der ikke er forandringer, springer vi videre til næste person
                    continue
                else:
                    opus_per.updated = True
                    persons_to_update[key] = opus_per
            # ellers indsættes en ny
            else:
                persons_to_insert[key] = opus_per
                #tilføj logning

        per_repo.insert_persons(persons_to_insert)
        per_repo.update_persons(persons_to_update)

        for key in sofd_persons:
            # Hvis en nøgle (cpr) er i SOFD men ikke i OPUS udtræk er det fordi personens stillinger alle er nedlagte
            if key not in opus_persons:
                per_repo.delete_person(key)

    def update_positions(self):
        '''
        Funktion der indsætter nye positions fra OPUS, 
        opdaterer positions hvor der er forandringer og sletter 
        positions som ikke længere er en del af vores lønsystem
        '''
        pos_repo = Position_repo(self.constr_lora)
        sofd_positions = pos_repo.get_positions('WHERE [deleted] = 0')
        opus_positions = self.get_positions()
        positions_to_insert = {}
        positions_to_update = {}

        # key er opus_id (medarbejdernummer)
        for key in opus_positions:
            opus_pos = opus_positions[key]
            # hvis stillingen findes, tjekkes den for forandringer
            if key in sofd_positions:
                sofd_pos = sofd_positions[key]
                if opus_pos.los_id == sofd_pos.los_id and opus_pos.person_ref == sofd_pos.person_ref and opus_pos.position_title == sofd_pos.position_title \
                        and opus_pos.position_id == sofd_pos.position_id and opus_pos.position_title_short == sofd_pos.position_title_short and \
                        opus_pos.position_paygrade_text == sofd_pos.position_paygrade_text and opus_pos.is_manager == sofd_pos.is_manager and \
                        opus_pos.payment_method == sofd_pos.payment_method and opus_pos.payment_method_text == sofd_pos.payment_method_text and \
                        opus_pos.weekly_hours_numerator == sofd_pos.weekly_hours_numerator and opus_pos.weekly_hours_denominator == sofd_pos.weekly_hours_denominator \
                        and opus_pos.invoice_recipient == sofd_pos.invoice_recipient and opus_pos.pos_pnr == sofd_pos.pos_pnr and opus_pos.dsuser == sofd_pos.dsuser \
                        and opus_pos.start_date == sofd_pos.start_date and opus_pos.leave_date == sofd_pos.leave_date:
                    # Når der ikke er forandringer, springer vi videre til næste position
                    continue
                else:
                    opus_pos.updated = True
                    positions_to_update[key] = opus_pos
            # ellers indsættes en ny
            else:
                positions_to_insert[key] = opus_pos

        for key in sofd_positions:
            # hvis en nøgle (opus_id) er i SOFD men ikke i OPUS udtræk er det fordi stillingen er nedlagt
            if key not in opus_positions:
                pos = sofd_positions[key]
                pos.deleted = True
                positions_to_update[key] = pos

        pos_repo.insert_positions(positions_to_insert)
        pos_repo.update_positions(positions_to_update)
        
