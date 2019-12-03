import json
import requests
from requests.auth import HTTPBasicAuth
from mox_clients.OS2Rollekatalog.json_models import Sts_collection_json, Orgunit_json, Manager_json, User_json, Position_json
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


class Os2rollekatalog_sync_service:
    def __init__(self, lora_constr):
        self.lora_constr = lora_constr

    def create_org_json(self):
        result = Sts_collection_json()
        org_repo = Orgunit_repo(self.lora_constr)
        pos_repo = Position_repo(self.lora_constr)
        per_repo = Person_repo(self.lora_constr)
        usr_repo = User_repo(self.lora_constr)
        orgs = org_repo.get_orgunits()
        poss = pos_repo.get_positions(
            'WHERE [uuid_userref] is not NULL and [deleted] = 0')
        pers = per_repo.get_persons()
        usrs = usr_repo.get_users()

        for los_id in orgs:
            sofd_org = orgs[los_id]
            sofd_manager = None
            jsman = None
            # den sidste del er pga de ledere der også er politikere som snyder med deres brugerkonti, det skal der egentligt rydes op i
            if sofd_org.manager_opus_id != None and int(sofd_org.manager_opus_id) in usrs:
                sofd_manager = usrs[int(sofd_org.manager_opus_id)]
                jsman = Manager_json(sofd_manager.uuid, sofd_manager.userid)
            jsorg = Orgunit_json(
                sofd_org.uuid, sofd_org.longname, sofd_org.parent_orgunit_uuid, jsman)
            result.add_org(jsorg)

        for opus_id in poss:
            sofd_pos = poss[opus_id]
            sofd_usr = usrs[opus_id]
            sofd_per = pers[sofd_pos.person_ref]
            sofd_org = orgs[sofd_pos.los_id]
            json_pos = Position_json(sofd_pos.position_title, sofd_org.uuid)
            json_usr = User_json(sofd_pos.uuid_userref, sofd_usr.userid,
                                 sofd_per.firstname + ' ' + sofd_per.lastname, sofd_usr.email)
            json_usr.add_position(json_pos)
            result.add_user(json_usr)
        return json.dumps(result.reprJSON(), cls=ComplexEncoder)

    def post_json(self, url, apikey, json_str):
        print(json_str)
        headers = {'content-type': 'application/json'}
        auth = HTTPBasicAuth('apiKey', apikey)
        req = requests.post(url=url, headers=headers, auth=auth,
                            data=json_str.encode('utf-8'))
