import xml.etree.ElementTree as ET
from service.orgunit_service import Orgunit_service
from model.employee import Employee
from pprint import pprint


os = Orgunit_service('c:\work\med_test.xml')
l = os.get_orgunits_from_xml()
print(len(l))


emps = 0
tree = ET.parse('c:\work\med_test.xml')
root = tree.getroot()

for emp in root.findall('employee'):
    emps = emps + 1
    if emps == 1:
        employee = Employee(emp.get('id'))

        pprint(vars(employee))


etst = Employee(123)
list1 = []
list1.append(etst)

x = next((x for x in list1 if x.opus_id == 1223), None)
print(x)
# pprint(vars(x))
