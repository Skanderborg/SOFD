from model.position import Position
from model.person import Person
import xml.etree.ElementTree as ET


class Employee_service:
    def __init__(self, xmlpath):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.persons = {}
        self.positions = []

    def build_people_and_positions(self):
        for emp in self.root.findall('employee'):
            if emp.get('action') == None:
                cpr = emp.find('cpr').text

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

                pos = Position(emp.get('id'),
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
                self.positions.append(pos)
            elif emp.get('action') == 'leave':
                continue

    def get_persons(self):
        return self.persons

    def get_positions(self):
        return self.positions
