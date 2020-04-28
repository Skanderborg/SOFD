import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.email_service import Email_service
from mox_clients.os2sync.os2sync_sync_service import Os2sync_sync_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
error_email = os.environ.get('error_email')
step = 'starting'

try:
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')
    os2sync_apikey = os.environ.get('os2sync_apikey')
    os2sync_orgunit_endpointurl = os.environ.get('os2sync_orgunit_endpointurl')
    os2sync_user_endpointurl = os.environ.get('os2sync_user_endpointurl')
    step = 'setup complete'


    os2sync_sync_service = Os2sync_sync_service(constr_lora, os2sync_apikey, os2sync_orgunit_endpointurl, os2sync_user_endpointurl)
    step = 'os2sync_sync_service created'
    
    os2sync_sync_service.sync_orgunits()
    step = 'orgunits synced successfully with os2sync'

    os2sync_sync_service.sync_users()
    step = 'users synced succesfully withos2sync'

except Exception as e:
    es.send_mail(error_email,
                 'Error: mox_os2sync.py python app', 'Step: ' + step + ' - Exception: ' + str(e))