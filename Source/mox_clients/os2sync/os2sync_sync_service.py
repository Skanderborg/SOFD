import json
import requests
from requests.auth import HTTPBasicAuth
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from dal.queue_users_repo import Queue_users_repo
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
    '''
    Os2Sync service håndterer selve synkroniseringen mod OS2Sync systemet. Den arbejder med queue.* tabellerne i databasen, og registerer
    successfulde hændelser i sykroniseringen som værende færdige i sts_org feltet.
    '''
    def __init__(self, constr_lora, apikey, orgunit_api_url, user_api_url):
        '''
        constructor, som har parametre der er en connection string til SOFD databasen: den api nøgle som identificere os i os2sync.
        api urls til orgunit og user api'erne.
        '''
        self.constr_lora = constr_lora
        self.org_repo = Orgunit_repo(self.constr_lora)
        self.apikey = apikey
        self.orgunit_api_url = orgunit_api_url
        self.user_api_url = user_api_url

    def sync_orgunits(self):
        '''
        funktion, der synkroniserer alle de orgunits, som er i køen. der kigges på sts_org feltet fordi det er her vi registerer om et queue item er sendt
        til sykronisering eller ej.
        '''
        queue_repo = Queue_orgunit_repo(self.constr_lora)
        queue = queue_repo.get_orgunit_queueitems("WHERE sts_org = 0")
        if(len(queue) > 0):
            # Engang imellem har IT ikke fået printet et UUID på en org enhed endnu
            orgs = self.org_repo.get_orgunits("WHERE [uuid] is not null")
            synced_queue_items = {}
            for system_id in queue:
                queue_item = queue[system_id]
                #tjekker key
                if queue_item.los_id not in orgs:
                    continue
                result = None
                if queue_item.change_type == 'Updated':
                    org = orgs[queue_item.los_id]
                    org_json = Orgunit_json(org.uuid, org.los_id, org.longname, org.parent_orgunit_uuid, '87947000', 'skanderborg.kommune@skanderborg.dk')
                    json_to_submit = json.dumps(org_json.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
                    result = Os2sync_sync_service.post_json(self, self.orgunit_api_url, json_to_submit)
                elif queue_item.change_type == 'Deleted':
                    end_point_url_delete = self.orgunit_api_url + '/' + queue_item.uuid
                    result = Os2sync_sync_service.delete_action(self, end_point_url_delete)

                if result == 200:
                    queue_item.sts_org = True
                    synced_queue_items[system_id] = queue_item
            queue_repo.update_queue_orgunits(synced_queue_items)

    def sync_users(self):
        '''
        funktion, der synkroniserer alle de users, som er i køen. der kigges på sts_org feltet fordi det er her vi registerer om et queue item er sendt
        til sykronisering eller ej.
        '''
        queue_repo = Queue_users_repo(self.constr_lora)
        queue = queue_repo.get_user_queues("WHERE sts_org = 0")
        if(len(queue) > 0):
            synced_queue_items = {}
            usr_repo = User_repo(self.constr_lora)
            per_repo = Person_repo(self.constr_lora)
            pos_repo = Position_repo(self.constr_lora)
            orgs = self.org_repo.get_orgunits()
            usrs = usr_repo.get_users()
            pers = per_repo.get_persons()
            poses = pos_repo.get_positions()
            for system_id in queue:
                queue_item = queue[system_id]
                if queue_item.change_type == 'Updated':
                    '''
                    Når en medarbejder forlader organisationen, bliver der typisk oprettet et "updated" event i opus, dagen før der oprettes et "deleted" event.
                    Hvis synkroniseirngen af en eller anden årsag går galt. Eller begge events kommer samme dag (kmd levere kun data 5 dage om ugen, så det kan poole)
                    vil denne "updated" stoppe synkroniseringen fordi stillingen slås op i pyt.positions når der skal opdateres. Her vil stillinge dog ikke længere være,
                    fordi den også er deleted - og et deleted event fjerne stillingen når eventet er føjet til køen.

                    Følgene IF sætning fikser det problem.
                    '''
                    if queue_item.opus_id not in poses or queue_item.opus_id not in usrs:
                        queue_item.change_type = 'Deleted'
                        synced_queue_items[system_id] = queue_item
                        continue
                    pos = poses[queue_item.opus_id]
                    if pos.person_ref not in pers:
                        queue_item.change_type = 'Deleted'
                        synced_queue_items[system_id] = queue_item
                        continue
                    usr = usrs[queue_item.opus_id]
                    per = pers[pos.person_ref]
                    org = orgs[pos.los_id]
                    person_json = Person_json(per.get_firstname_including_displayname() + ' ' + per.get_lastname_including_displayname(), per.cpr)
                    position_json = Position_json(org.uuid, org.longname)
                    usr_json = User_json(pos.uuid_userref, usr.userid, usr.email, org.longname, queue_item.opus_id, usr.phone)
                    usr_json.add_person(person_json)
                    usr_json.add_position(position_json)
                    json_to_submit = json.dumps(usr_json.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
                    result = Os2sync_sync_service.post_json(self, self.user_api_url, json_to_submit)
                    if result == 200:
                        queue_item.sts_org = True
                        synced_queue_items[system_id] = queue_item
                    # det følgende opdaterer status i DB per enhed, i stedet for at tage dem i et ruf. Kan bruges når der er MANGE i kø
                    #if result == 200:
                    #    queue_item.sts_org = True
                    #    queue_repo.update_queue_user(queue_item)

                elif queue_item.change_type == 'Deleted':
                    #print('deleted')
                    end_point_url_delete = self.user_api_url + '/' + queue_item.uuid
                    result = Os2sync_sync_service.delete_action(self, end_point_url_delete)
                    if result == 200:
                        queue_item.sts_org = True
                        synced_queue_items[system_id] = queue_item
                    # det følgende opdaterer status i DB per enhed, i stedet for at tage dem i et ruf. Kan bruges når der er MANGE i kø
                    #if result == 200:
                    #    queue_item.sts_org = True
                    #    queue_repo.update_queue_user(queue_item)
            queue_repo.update_queue_users(synced_queue_items)
                




    def post_json(self, endpoint_url, json_str):
        #print(endpoint_url)
        #print(json_str)
        headers = {'content-type': 'application/json', 'ApiKey': self.apikey}
        res = requests.post(url=endpoint_url, headers=headers, data=json_str)
        #print('request - body: ', res.request.body)
        #print('request - headers: ', res.request.headers)
        #print('response - text: ', res.text)
        #print('response - status code: ', res.status_code)
        return res.status_code

    def get_action(self):
        #return 301
        headers = {'content-type': 'application/json', 'ApiKey': self.apikey}
        res = requests.get(url='https://skanderborg.os2sync.dk/api/orgUnit/840404b6-efd9-4356-8d4d-b8502442c316',  headers=headers)
        #res = requests.get(url='https://skanderborg.os2sync.dk/api/user/838df441-1a7f-4ccf-9869-51b1758853e0',  headers=headers)
        print('response - text: ', res.text)
        print('response - status code: ', res.status_code)

    def delete_action(self, endpoint_url):
        headers = {'ApiKey': self.apikey}
        req = requests.delete(url=endpoint_url, headers=headers)
        #print('request - text', req.text)
        #print('request - status code', req.status_code)
        return req.status_code