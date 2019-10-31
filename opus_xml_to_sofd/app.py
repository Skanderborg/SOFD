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
Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse
'''
# sætter .env op
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
step = 'starting'
try:
    # henter stien til den sti hvor vores kfs-lan udtræk for OPUS medarbejder data er placeret
    xml_path = os.environ.get('employee_org_xml_path')
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')

    # finder frem til den seneste fil fra OPUS
    list_of_files = glob.glob(xml_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    step = 'setup complete'

    # opdaterer orgunits fra OPUS til SOFD
    org_service = Orgunit_service(latest_file, constr_lora)
    org_service.update_orgunits()
    step = 'org units complete'

    # opdaterer employee fra OPUS til position og person i SOFD
    emp_service = Employee_service(latest_file, constr_lora)
    emp_service.build_people_and_positions_from_opusxml()
    step = 'build pos + per complete'
    emp_service.update_persons()
    step = 'update persons complete'
    emp_service.update_positions()
    step = 'update positions complete'
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus python - update_positions()', step)
