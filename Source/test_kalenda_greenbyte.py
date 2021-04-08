import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kalenda_greenbyte.kalenda_greenbyte_sync_service import Kalenda_greenbyte_sync_service

#setup env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
#laod db constr
constr_lora = os.environ.get('constr_lora')

#Kalenda_greenbyte SOFD Sync
kalenda_greenbyte_endpointurl = os.environ.get('kalenda_greenbyte_endpointurl_test')
kalenda_greenbyte_apikey = os.environ.get('kalenda_greenbyte_apikey')
kalenda_greenbyte_parent_los_id = os.environ.get('kalenda_greenbyte_parent_los_id')
kalenda_greenbyte_mox_client = Kalenda_greenbyte_sync_service(constr_lora)
kalenda_greenbyte_mox_client.post_json(kalenda_greenbyte_endpointurl, kalenda_greenbyte_apikey, kalenda_greenbyte_parent_los_id)