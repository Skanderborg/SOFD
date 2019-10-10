import xml.etree.ElementTree as ET
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service
from pprint import pprint


os = Orgunit_service('c:\work\med_test.xml')
l = os.get_orgunits_from_xml()
print(len(l))

es = Employee_service('c:\work\med_test.xml')
es.build_people_and_positions()
per = es.get_people()
pos = es.get_positions()
print(len(per))
print(len(pos))

# pprint(vars(per['']))
# pprint(vars(x))
