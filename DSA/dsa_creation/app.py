import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
xml_path = os.environ.get('employee_org_xml_path')
print(xml_path)



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
