import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from service.opus_xml_to_sofd.orgunit_service import Orgunit_service
from service.opus_xml_to_sofd.employee_service import Employee_service
from service.email_service import Email_service

'''
python app that builds the SOFD from the OPUS XML export.
Needs to run before anything else.
author - Jacob Ågård Bennike
Skanderborg Kommune 2019
'''
# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
error_email = os.environ.get('error_email')
step = 'starting'

try:
    # henter stien til den sti hvor vores kfs-lan udtræk for OPUS medarbejder data er placeret
    xml_path = os.environ.get('employee_org_xml_path')
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')
    # finder los_id på top organisationen (Skanderborg Kommune) - dette ændre sig næppe, men hvis det gør skal det kunne opdateres
    # skal anvendes som int
    skb_top_organisation_los_id = int(os.environ.get('skb_top_organisation_los_id'))

    # finder frem til den seneste fil fra OPUS
    list_of_files = glob.glob(xml_path)
    latest_file = max(list_of_files, key=os.path.getctime)
    step = 'setup complete'

    # opdaterer orgunits fra OPUS til SOFD
    org_service = Orgunit_service(latest_file, constr_lora)
    org_service.update_orgunits(skb_top_organisation_los_id)
    step = 'org_service.update_orgunits() complete'

    # opdaterer employee fra OPUS til position og person i SOFD
    emp_service = Employee_service(latest_file, constr_lora)
    emp_service.build_people_and_positions_from_opusxml()
    step = 'build pos + per complete'
    emp_service.update_persons()
    step = 'update persons complete'
    emp_service.update_positions()
    step = 'update positions complete'
except Exception as e:
   es.send_mail(error_email,
                 'Error: opus_xml_to_sofd python app', 'Step: ' + step + ' - Exception: ' + str(e))