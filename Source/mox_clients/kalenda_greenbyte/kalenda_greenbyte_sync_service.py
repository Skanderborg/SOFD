import json
import requests
from requests.auth import HTTPBasicAuth
from mox_clients.kalenda_greenbyte.json_models import Collection_json, Orgunit_json, Employee_json
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

class Kalenda_greenbyte_sync_service:
    def __init__(self, lora_constr):
        self.lora_constr = lora_constr

    def create_org_json(self, top_org_los_id):
        '''
        Funktion som generere den json, der skals endes til kalenda-greenbyte, ud fra json_modellerne og vores SOFD
        Der hentes data fra person, user, position og orgunit tabellerne.
        '''
        result = Collection_json()
        per_repo = Person_repo(self.lora_constr)
        usr_repo = User_repo(self.lora_constr)
        orgs = Kalenda_greenbyte_sync_service.get_orgunits(self, top_org_los_id)
        poss = Kalenda_greenbyte_sync_service.get_poisitions(self, orgs)
        pers = per_repo.get_persons()
        usrs = usr_repo.get_users()

        for los_id in orgs:
            sofd_org = orgs[los_id]
            jsorg = Orgunit_json(sofd_org.los_id, sofd_org.parent_orgunit_los_id, sofd_org.longname, sofd_org.pnr)
            result.add_org(jsorg)

        for opus_id in poss:
            sofd_pos = poss[opus_id]
            sofd_usr = usrs[opus_id]
            sofd_per = pers[sofd_pos.person_ref]
            sofd_org = orgs[sofd_pos.los_id]
            json_emp = Employee_json(opus_id, sofd_pos.los_id, sofd_per.firstname, sofd_per.lastname, sofd_usr.email,
                                        sofd_usr.userid, sofd_pos.uuid_userref, sofd_pos.is_manager, sofd_pos.kmd_suppid,
                                        sofd_per.cpr, sofd_pos.payment_method, sofd_org.pnr)
            result.add_emp(json_emp)
        result = json.dumps(result.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def get_orgunits(self, top_org_los_id):
        '''
        Henter de relevante orgunits, fra en bestemt rod. Det sker fordi det kun er et bestemt område
        af organisationen, som skal synkroniseres med kalenda-greenbyte.
        Dette sher ud fra los_id, som kan findes i .env filen.
        Hvis der skiftes rundt i LOS, skal dette ID opdateres.
        '''
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
        '''
        Funktion som rekursivt tjekker om en orgunit er under den organisations enhed som danner rod for
        de orgunits som skal synkroniseres.
        '''
        if org.parent_orgunit_los_id == 0:
            return False
        elif org.parent_orgunit_los_id == top_org_los_id:
            return True
        else:
            org = orgs[org.parent_orgunit_los_id]
            return Kalenda_greenbyte_sync_service.org_recursion(self, top_org_los_id, orgs, org)

    def get_poisitions(self, orgs):
        '''
        Funktion som finder de positions, der hører til en af de orgunits som skal synkroniseres med kalenda-greenbyte
        '''
        pos_repo = Position_repo(self.lora_constr)
        poss = pos_repo.get_positions(
            'WHERE [uuid_userref] is not NULL and [deleted] = 0 and [ad_user_deleted] = 0')
        result = {}
        for opus_id in poss:
            pos = poss[opus_id]
            if pos.los_id in orgs:
                result[opus_id] = pos
        return result

    def print_json(self, top_org_los_id):
        '''
        Test funktion til at se json
        '''
        json_str = Kalenda_greenbyte_sync_service.create_org_json(self, top_org_los_id)
        print(json_str.decode())

    def post_json(self, url, apikey, top_org_los_id):
        '''
        Sender data til kalenda-greenbyte - anvender url, apikey og top_org_los_id som findes i .env
        '''
        json_str = Kalenda_greenbyte_sync_service.create_org_json(self, top_org_los_id)
        headers = {'content-type': 'application/json', 'ApiKey': apikey}
        #print(json_str)
        req = requests.post(url=url, headers=headers, data=json_str)
        #print(req.text)
        #print(req.status_code)
        return req.status_code