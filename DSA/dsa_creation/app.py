import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
xml_path = os.environ.get('employee_org_xml_path')
constr_lora = os.environ.get('constr_lora')


emp_service = Employee_service(xml_path, constr_lora)
emp_service.build_people_and_positions()
emp_service.insert_persons()

#orgunit_service = Orgunit_service('c:\work\med_test.xml')
#l = orgunit_service.get_orgunits_from_xml()
# print(len(l))

#es = Employee_service('c:\work\med_test.xml')
# es.build_people_and_positions()
#per = es.get_persons()
#pos = es.get_positions()
# print(len(per))
# print(len(pos))

#constr = os.environ.get('constr_lora')
#pr = Person_repo(constr)
# pr.Get_persons()

# pprint(vars(per['']))
# pprint(vars(x))
