import os
from os.path import join, dirname
from dotenv import load_dotenv
from mox_clients.os2sync.os2sync_sync_service import Os2sync_sync_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')
os2sync_apikey = os.environ.get('os2sync_apikey')
os2sync_orgunit_endpointurl = os.environ.get('os2sync_orgunit_endpointurl')
os2sync_user_endpointurl = os.environ.get('os2sync_user_endpointurl')

os2sync_sync_service = Os2sync_sync_service(constr_lora, os2sync_apikey, os2sync_orgunit_endpointurl, os2sync_user_endpointurl)
print('orgs')
os2sync_sync_service.sync_orgunits()
print('users')
os2sync_sync_service.sync_users()
#os2sync_sync_service.get_action()