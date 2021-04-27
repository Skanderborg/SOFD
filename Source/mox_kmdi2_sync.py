import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kmdi2_sync.kmdi2_employee_api import Kmdi2_employee_api
from mox_clients.kmdi2_sync.kmd_institution_api import Kmd_institution_api
from mox_clients.kmdi2_sync.kmdi2_service import Kmdi2_service
from service.email_service import Email_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
kmdi2_test_key = os.environ.get('kmdi2_test_key')
kmdi2_employee_api_key = os.environ.get('kmdi2_employee_api_key')
kmdi2_api_key = os.environ.get('kmdi2_api_key')

#email setup
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
error_email = os.environ.get('error_email')

try:
    add_employee_url = os.environ.get('kmdi2_employee_api_endpoint') + 'employment/institution/'
    delete_employee_url = os.environ.get('kmdi2_employee_api_delete_endpoint')
    get_employements_url = os.environ.get('kmdi2_employee_api_endpoint') + "employments"
    constr_lora = os.environ.get('constr_lora')
    kmdi2_service = Kmdi2_service(constr_lora)
    kmdi2_service.sync_employees_with_kmdi2(kmdi2_employee_api_key, add_employee_url, get_employements_url, delete_employee_url)
except Exception as e:
    es.send_mail(error_email,
                 'Error: mox_kmdi2_sync.py python app', 'Exception: ' + str(e))