import json
import requests

import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob

#setup env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
endpoint_url = os.environ.get('azure')


json_str = '[{"Fornavn":"jacob","Efternavn":"test","IsCura":"False"}]'


headers = {'content-type': 'application/json'}
res = requests.post(url=endpoint_url, headers=headers, data=json_str)

print('request - body: ', res.request.body)
print('request - headers: ', res.request.headers)
print('response - text: ', res.text)
print('response - status code: ', res.status_code)