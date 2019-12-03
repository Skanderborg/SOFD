import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.OS2Rollekatalog.os2rollekatalog_sync_service import Os2rollekatalog_sync_service
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
constr_lora = os.environ.get('constr_lora')
api_key = os.environ.get('os2rollekatalog_apikey')
endpointurl = os.environ.get('os2rollekatalog_endpointurl')


oss = Os2rollekatalog_sync_service(constr_lora)
json_str = oss.create_org_json()
#oss.post_json(endpointurl, api_key, json_str)
