import json
import requests
from requests.auth import HTTPBasicAuth
from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit
from mox_clients.os2sync.json_models import Orgunit_json, Generic_address_json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class Os2sync_sync_service:
    def __init__(self, constr_lora, apikey, orgunit_api_url):
        self.constr_lora = constr_lora
        self.org_repo = Orgunit_repo(self.constr_lora)
        self.apikey = apikey
        self.orgunit_api_url = orgunit_api_url

    def sync_orgunits(self):
        queue_repo = Queue_orgunit_repo(self.constr_lora)
        queue = queue_repo.get_orgunit_queueitems('WHERE sts_org = 0')

        if(len(queue) > 0):
            orgs = self.org_repo.get_orgunits()
            synced_queue_items = {}
            for system_id in queue:
                item = queue[system_id]
                org = orgs[item.los_id]
                result = None
                if item.change_type == 'Updated':
                    phone = Generic_address_json(org.phonenumber)
                    email = Generic_address_json('skanderborg.kommune@skanderborg.dk')
                    org_json = Orgunit_json(org.uuid, org.los_id, org.longname, org.parent_orgunit_uuid, org.startdate, phone, email)
                    json_to_submit = json.dumps(org_json.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
                    result = Os2sync_sync_service.post_json(self, json_to_submit)
                elif item.change_type == 'Deleted':
                    print('deleted')

                if result == 200:
                    item.sts_org = True
                    synced_queue_items[system_id] = item
                queue_repo.update_queue_orgunits(synced_queue_items)

    def post_json(self, json_str):
        headers = {'content-type': 'application/json', 'ApiKey': self.apikey}
        req = requests.post(url=self.orgunit_api_url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code