import json
import requests
from requests.auth import HTTPBasicAuth
from mox_clients.kalenda_greenbyte.json_models import Collection_json, Orgunit_json, Employee_json
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class Kalenda_greenbyte_sync_service:
    def __init__(self, lora_constr):
        self.lora_constr = lora_constr

    def create_org_json(self, top_org_los_id):
        result = Collection_json()
        per_repo = Person_repo(self.lora_constr)
        usr_repo = User_repo(self.lora_constr)
        orgs = Kalenda_greenbyte_sync_service.get_orgunits(self, top_org_los_id)
        poss = Kalenda_greenbyte_sync_service.get_poisitions(self, orgs)
        pers = per_repo.get_persons()
        usrs = usr_repo.get_users()

        for los_id in orgs:
            sofd_org = orgs[los_id]
            jsorg = Orgunit_json(sofd_org.los_id, sofd_org.parent_orgunit_los_id, sofd_org.longname)
            result.add_org(jsorg)

        for opus_id in poss:
            sofd_pos = poss[opus_id]
            sofd_usr = usrs[opus_id]
            sofd_per = pers[sofd_pos.person_ref]
            json_emp = Employee_json(opus_id, sofd_pos.los_id, sofd_per.firstname, sofd_per.lastname, sofd_usr.email,
                                        sofd_usr.userid, sofd_pos.uuid_userref, sofd_pos.is_manager)
            result.add_emp(json_emp)
        result = json.dumps(result.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def get_orgunits(self, top_org_los_id):
        top_org_los_id = int(top_org_los_id)
        org_repo = Orgunit_repo(self.lora_constr)
        orgs = org_repo.get_orgunits()
        result = {}
        for los_id in orgs:
            org = orgs[los_id]
            if Kalenda_greenbyte_sync_service.org_recursion(self, top_org_los_id, orgs, org) == True:
                result[los_id] = org
        return result

    def org_recursion(self, top_org_los_id, orgs, org):
        if org.parent_orgunit_los_id == 0:
            return False
        elif org.parent_orgunit_los_id == top_org_los_id:
            return True
        else:
            org = orgs[org.parent_orgunit_los_id]
            return Kalenda_greenbyte_sync_service.org_recursion(self, top_org_los_id, orgs, org)

    def get_poisitions(self, orgs):
        pos_repo = Position_repo(self.lora_constr)
        poss = pos_repo.get_positions(
            'WHERE [uuid_userref] is not NULL and [deleted] = 0')
        result = {}
        for opus_id in poss:
            pos = poss[opus_id]
            if pos.los_id in orgs:
                result[opus_id] = pos
        return result

    def print_json(self, top_org_los_id):
        json_str = Kalenda_greenbyte_sync_service.create_org_json(self, top_org_los_id)
        print(json_str.decode())

    def post_json(self, url, apikey, top_org_los_id):
        json_str = Kalenda_greenbyte_sync_service.create_org_json(self, top_org_los_id)
        headers = {'content-type': 'application/json', 'ApiKey': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code