from model.position import Position
from model.person import Person
from dal.person_repo import Person_repo
from dal.position_repo import Position_repo
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pprint import pprint

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
        This function reads the OPUS XML and splits the "employee" tag into two dictionaries, one for person objects and one for position objects.
        The person key is CPR
        The position key is OPUS ID (employee ID)
        both are unique.
        Positions are tied to persons in a many to one relationship that gets registered on position through the CPR.

        OBS: This script doesn't handle CPR changes. The OPUS system that supplies the data isn't woke enough to handle this, however, so it's not a problem right now.
        '''
        pos_repo = Position_repo(self.constr_lora)
        disabled_orgs = pos_repo.get_disabled_orgunits()
        for emp in self.root.findall('employee'):
            if emp.get('action') == None:
                cpr = emp.find('cpr').text
                opus_id = emp.get('id')
                los_id = emp.find('orgUnit').text
                if los_id in disabled_orgs:
                    continue

                userId = None
                if emp.find('userId') != None:
                    userId = emp.find('userId').text

                startdate = None
                if emp.find('entryDate') != None:
                    startdate = emp.find('entryDate').text
                elif emp.find('initialEntry') != None:
                    startdate = emp.find('initialEntry').text
                elif emp.find('entryIntoGroup') != None:
                    startdate = emp.find('entryIntoGroup').text

                if startdate == None:
                    continue
                else:
                    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()

                leavedate = None
                if emp.find('leaveDate') != None:
                    leaveDate = emp.find('leaveDate').text

                per = Person(cpr,
                             emp.find('firstName').text,
                             emp.find('lastName').text,
                             emp.find('address').text,
                             emp.find('postalCode').text,
                             emp.find('city').text,
                             emp.find('country').text)

                pos = Position(opus_id,
                               los_id,
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
                               startdate,
                               leavedate)

                self.persons[cpr] = per
                self.positions[int(opus_id)] = pos
            elif emp.get('action') == 'leave':
                continue

    def get_persons(self):
        return self.persons

    def get_positions(self):
        return self.positions

    def update_persons(self):
        '''
        Function to insert new persons from OPUS, update people who have changed and mark absent people as deleted to be handled later because they are tied to positions
        '''
        per_repo = Person_repo(self.constr_lora)
        sofd_persons = per_repo.get_persons()
        opus_persons = self.get_persons()

        for key in opus_persons:
            opus_per = opus_persons[key]

            if key in sofd_persons:
                sofd_per = sofd_persons[key]
                if opus_per.firstname == sofd_per.firstname and opus_per.lastname == sofd_per.lastname and opus_per.address == sofd_per.address \
                        and opus_per.zipcode == sofd_per.zipcode and opus_per.city == sofd_per.city and opus_per.country == sofd_per.country:
                    continue
                else:
                    per_repo.update_person(opus_per)
            else:
                per_repo.insert_person(opus_per)

        for key in sofd_persons:
            if key not in opus_persons:
                per_repo.delete_person(key)

    def update_positions(self):
        '''
        Function to insert new positions from OPUS, update people who have changed and mark absent positions as deleted to be handled later because they are tied to persons
        '''
        pos_repo = Position_repo(self.constr_lora)
        sofd_positions = pos_repo.get_positions()
        opus_positions = self.get_positions()

        for key in opus_positions:
            opus_pos = opus_positions[key]
            if key in sofd_positions:
                sofd_pos = sofd_positions[key]
                if opus_pos.los_id == sofd_pos.los_id and opus_pos.person_ref == sofd_pos.person_ref and opus_pos.position_title == sofd_pos.position_title \
                        and opus_pos.position_id == sofd_pos.position_id and opus_pos.position_title_short == sofd_pos.position_title_short and \
                        opus_pos.position_paygrade_text == sofd_pos.position_paygrade_text and opus_pos.is_manager == sofd_pos.is_manager and \
                        opus_pos.payment_method == sofd_pos.payment_method and opus_pos.payment_method_text == sofd_pos.payment_method_text and \
                        opus_pos.weekly_hours_numerator == sofd_pos.weekly_hours_numerator and opus_pos.weekly_hours_denominator == sofd_pos.weekly_hours_denominator \
                        and opus_pos.invoice_recipient == sofd_pos.invoice_recipient and opus_pos.pos_pnr == sofd_pos.pos_pnr and opus_pos.dsuser == sofd_pos.dsuser \
                        and opus_pos.start_date == sofd_pos.start_date and opus_pos.leave_date == sofd_pos.leave_date:
                    continue
                else:
                    pos_repo.update_position(opus_pos)
            else:
                pos_repo.insert_position(opus_pos)

        for key in sofd_positions:
            if key not in opus_positions:
                pos_repo.delete_position(key)
