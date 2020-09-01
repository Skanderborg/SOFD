import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.os2rollekatalog.os2rollekatalog_sync_service import Os2rollekatalog_sync_service
from service.email_service import Email_service

'''
Mox klient som synkroniserer org data med OS2Rollekataloget.
'''
# henter variable fra .env filen
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
constr_lora = os.environ.get('constr_lora')
api_key = os.environ.get('os2rollekatalog_apikey')
endpointurl = os.environ.get('os2rollekatalog_endpointurl')
error_email = os.environ.get('error_email')

# email service
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))

# kører service
try:
    oss = Os2rollekatalog_sync_service(constr_lora)
    step = 'Json'
    json_str = oss.create_org_json()
    step = 'api'
    status_code = oss.post_json(endpointurl, api_key, json_str)
    step = 'status_code'
    if status_code != 200:
        es.send_mail(error_email,
                 'Error: mox_os2rollekatalog_sync.py python app', 'Step = ' + step + ': ' + status_code)
except Exception as e:
    es.send_mail(error_email,
                 'Error: mox_os2rollekatalog_sync.py python app', 'Step = ' + step + ' - Exception: ' + str(e))