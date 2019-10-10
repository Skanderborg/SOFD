from model.position import Position
from model.person import Person
import xml.etree.ElementTree as ET


class Employee_service:
    def __init__(self, xmlpath):
        self.tree = ET.parse(xmlpath)
        self.root = self.tree.getroot()
        self.people = {}
        self.positions = []

    def build_people_and_positions(self):
        for emp in self.root.findall('employee'):
            if emp.get('action') == None:
                cpr = emp.find('cpr').text

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
                             emp.find('lastName').text)

                pos = Position(cpr,
                               emp.get('id'),
                               emp.get('lastChanged'),
                               emp.find('position').text,
                               emp.find('positionShort').text,
                               emp.find('orgUnit').text,
                               emp.find('payGradeText').text,
                               emp.find('numerator').text,
                               emp.find('denominator').text,
                               emp.find('isManager').text,
                               emp.find('workContract').text,
                               emp.find('workContractText').text,
                               entryDate,
                               leaveDate,
                               intialEntry,
                               entryIntoGroup)
                self.people[cpr] = per
                #self.people.append(cpr, per)
                self.positions.append(pos)
            elif emp.get('action') == 'leave':
                continue

    def get_people(self):
        return self.people

    def get_positions(self):
        return self.positions
