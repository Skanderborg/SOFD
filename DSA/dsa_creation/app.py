from dal.position_repo import Position_repo
import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service
import glob

'''
python app that builds the SOFD from the OPUS XML export
author - Jacob Ågård Bennike
Skanderborg Kommune 2019
'''

'''
Enables and setsup the use of .env files, which is where we keep our secret stuff. This means you'll need to setup your own .env
containing the required values.
'''
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# sti til opus xml udtræk for medarbejdere
xml_path = os.environ.get('employee_org_xml_path')
# connection string til sofd databasen
constr_lora = os.environ.get('constr_lora')

# finder filnavnet på den seneste nye fil fra kmd på kfs-lan
list_of_files = glob.glob(xml_path)
latest_file = max(list_of_files, key=os.path.getctime)

# bygger orgunits
org_service = Orgunit_service(latest_file, constr_lora)
org_service.update_orgunits()

# bygger persons og positions
emp_service = Employee_service(latest_file, constr_lora)
emp_service.build_people_and_positions_from_opusxml()
emp_service.update_persons()
emp_service.update_positions()
