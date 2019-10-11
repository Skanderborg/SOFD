from model.position import Position
from model.person import Person
from dal.person_repo import Person_repo
import xml.etree.ElementTree as ET


class Employee_service:
    def __init__(self, xmlpath, constr_lora):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.constr_lora = constr_lora
        self.persons = {}
        self.positions = {}

    def build_people_and_positions_from_opusxml(self):
        '''
        This function reads the OPUS XML and splits the "employee" tag into two dictionaries, one for person objects and one for position objects.
        The person key is CPR
        The position key is OPUS ID (employee ID)
        both are unique.
        Positions are tied to persons in a many to one relationship that gets registered on position through the CPR.

        OBS: This script doesn't handle CPR changes. The OPUS system that supplies the data isn't woke enough to handle this, however, so it's not a problem right now.
        '''
        for emp in self.root.findall('employee'):
            if emp.get('action') == None:
                cpr = emp.find('cpr').text
                opus_id = emp.get('id')

                userId = None
                if emp.find('userId') != None:
                    userId = emp.find('userId').text

                entryDate = None
                if emp.find('entryDate') != None:
                    entryDate = emp.find('entryDate').text

                leaveDate = None
                if emp.find('leaveDate') != None:
                    leaveDate = emp.find('leaveDate').text

                intialEntry = None
                if emp.find('initialEntry') != None:
                    intialEntry = emp.find('initialEntry').text

                entryIntoGroup = None
                if emp.find('entryIntoGroup') != None:
                    entryIntoGroup = emp.find('entryIntoGroup').text

                per = Person(cpr,
                             emp.find('firstName').text,
                             emp.find('lastName').text,
                             emp.find('address').text,
                             emp.find('postalCode').text,
                             emp.find('city').text,
                             emp.find('country').text)

                pos = Position(opus_id,
                               emp.find('orgUnit').text,
                               cpr,
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
                               entryDate,
                               leaveDate,
                               intialEntry,
                               entryIntoGroup,
                               emp.get('lastChanged'))

                self.persons[cpr] = per
                self.positions[opus_id] = pos
            elif emp.get('action') == 'leave':
                continue

    def get_persons(self):
        return self.persons

    def get_positions(self):
        return self.positions

    def update_persons(self):
        '''
        Function that inserts new persons and updates old ones
        '''
        repo = Person_repo(self.constr_lora)
        sofd_persons = repo.get_persons()
        opus_persons = self.get_persons()

        for key in opus_persons:
            opus_per = opus_persons[key]
            if opus_per.firstname == None:
                opus_per.firstname = "Intet navn"
            if opus_per.lastname == None:
                opus_per.lastname = "Intet navn"
            if opus_per.address == None:
                opus_per.address = "Ingen addresse"
            if opus_per.zipcode == None:
                opus_per.zipcode = "Intet postnr"
            if opus_per.city == None:
                opus_per.city = "Ingen by"
            if opus_per.country == None:
                opus_per.country = "None"

            if key in sofd_persons:
                sofd_per = sofd_persons[key]
                if opus_per.firstname == sofd_per.firstname and opus_per.lastname == sofd_per.lastname and opus_per.address == sofd_per.address \
                        and opus_per.zipcode == sofd_per.zipcode and opus_per.city == sofd_per.city and opus_per.country == sofd_per.country:
                    continue
                else:
                    repo.update_person(opus_per)
            else:
                repo.insert_person(opus_per)

        for key in sofd_persons:
            if key not in opus_persons:
                repo.delete_person(key)
