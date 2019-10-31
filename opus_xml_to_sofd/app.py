from dal.position_repo import Position_repo
import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.orgunit_service import Orgunit_service
from service.employee_service import Employee_service
import glob
from service.email_service import Email_service

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


es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))

# bygger orgunits
org_service = Orgunit_service(latest_file, constr_lora)
try:
    org_service.update_orgunits()
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus python - update_orgunits()', 'something went wrong')

# bygger persons og positions
emp_service = Employee_service(latest_file, constr_lora)
try:
    emp_service.build_people_and_positions_from_opusxml()
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus python - build_people_and_positions_from_opusxml()', 'something went wrong')
try:
    emp_service.update_persons()
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus python - update_persons()', 'something went wrong')
try:
    emp_service.update_positions()
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus python - update_positions()', 'something went wrong')
