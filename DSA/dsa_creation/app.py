import xml.etree.ElementTree as ET
from model.orgunit import Orgunit
from pprint import pprint


tree = ET.parse('c:\work\med_test.xml')
root = tree.getroot()

orgs = 0
emps = 0

for orgunit in root.findall('orgUnit'):
    orgs = orgs + 1
    if orgs == 1:
        org = Orgunit(orgunit.get('id'),
                      orgunit.get('lastChanged'),
                      orgunit.find('longName').text,
                      orgunit.find('startDate').text,
                      orgunit.find('endDate').text,
                      orgunit.find('parentOrgUnit').text,
                      orgunit.find('shortName').text,
                      orgunit.find('street').text,
                      orgunit.find('zipCode').text,
                      orgunit.find('city').text,
                      orgunit.find('phoneNumber').text,
                      orgunit.find('cvrNr').text,
                      orgunit.find('eanNr').text,
                      orgunit.find('seNr').text,
                      orgunit.find('pNr').text,
                      orgunit.find('orgType').text,
                      orgunit.find('orgTypeTxt').text)
        pprint(vars(org))


for emp in root.findall('employee'):
    emps = emps + 1
