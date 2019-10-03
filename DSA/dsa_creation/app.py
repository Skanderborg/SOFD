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
        los_id = orgunit.get('id')
        last_changed = orgunit.get('lastChanged')
        longname = orgunit.find('longName').text
        org = Orgunit(los_id, last_changed, longname)
        pprint(vars(org))


for emp in root.findall('employee'):
    emps = emps + 1
