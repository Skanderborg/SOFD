from dal.position_repo import Position_repo
import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
xml_path = os.environ.get('employee_org_xml_path')
constr_lora = os.environ.get('constr_lora')


org_service = Orgunit_service(xml_path, constr_lora)
org_service.update_orgunits()

emp_service = Employee_service(xml_path, constr_lora)
emp_service.build_people_and_positions_from_opusxml()
emp_service.update_persons()
emp_service.update_positions()
