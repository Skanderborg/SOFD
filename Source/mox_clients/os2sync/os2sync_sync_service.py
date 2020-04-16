import json
import requests
from requests.auth import HTTPBasicAuth
from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit
from mox_clients.os2sync.json_models import Orgunit_json, User_json, Person_json, Position_json

class ComplexEncoder(json.JSONEncoder):
    '''
    JSON decoder, udvidelse til pythons json bibliotek, anvendes fordi nogle af vores objekter kan indeholde objekter, noget
    der som standard ikke kan håndteres i pythons standard bibliotek. Dette giver os samtidig bedre mulighed for at styrer
    navngivningen af Json attributerne.
    # pylint: disable=E0202 - er fordi Visual Studio Codes pylint giver falsepositive på "An attribute affected in %s line %s hide this method"
    '''
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
        queue = queue_repo.get_orgunit_queueitems('WHERE los_id = 1030006')

        if(len(queue) > 0):
            orgs = self.org_repo.get_orgunits()
            synced_queue_items = {}
            for system_id in queue:
                item = queue[system_id]
                org = orgs[item.los_id]
                result = None
                if item.change_type == 'Updated':
                    org_json = Orgunit_json(org.uuid, org.los_id, org.longname, org.parent_orgunit_uuid, '87947000', 'skanderborg.kommune@skanderborg.dk')

                    json_to_submit = json.dumps(org_json.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
                    result = Os2sync_sync_service.post_json(self, self.orgunit_api_url, json_to_submit)
                elif item.change_type == 'Deleted':
                    print('deleted')

                if result == 200:
                    item.sts_org = True
                    synced_queue_items[system_id] = item
                    queue_repo.update_queue_orgunits(synced_queue_items)

    def post_json(self, endpoint_url, json_str):
        headers = {'content-type': 'application/json', 'ApiKey': self.apikey}
        req = requests.post(url=endpoint_url, headers=headers, data=json_str)
        print('request - text', req.text)
        print('request - status code', req.status_code)
        return req.status_code