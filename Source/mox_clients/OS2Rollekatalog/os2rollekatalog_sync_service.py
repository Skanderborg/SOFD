import json
import requests
from requests.auth import HTTPBasicAuth
from mox_clients.os2rollekatalog.json_models import Sts_collection_json, Orgunit_json, Manager_json, User_json, Position_json
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo


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
            'WHERE [uuid_userref] is not NULL and [deleted] = 0 and [ad_user_deleted] = 0')
        pers = per_repo.get_persons()
        usrs = usr_repo.get_users()

        for los_id in orgs:
            sofd_org = orgs[los_id]
            if sofd_org.uuid is None or len(sofd_org.uuid) < 1:
                continue
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
            if sofd_usr.userid is None or len(sofd_usr.userid) < 1:
                continue
            sofd_per = pers[sofd_pos.person_ref]
            if sofd_pos.los_id not in orgs:
                continue
            sofd_org = orgs[sofd_pos.los_id]
            if sofd_org.uuid is None or len(sofd_org.uuid) <1:
                continue
            json_pos = Position_json(sofd_pos.position_title, sofd_org.uuid)
            json_usr = User_json(sofd_pos.uuid_userref, sofd_usr.userid,
                                 sofd_per.firstname + ' ' + sofd_per.lastname, sofd_usr.email)
            json_usr.add_position(json_pos)
            result.add_user(json_usr)
        result = json.dumps(result.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def post_json(self, url, apikey, json_str):
        headers = {'content-type': 'application/json', 'ApiKey': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code