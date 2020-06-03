from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit

class Orgunit_queue_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def update_orgunit_queue(self):
        # funktion som bearbejder alle orgunits som er enten opdaterede eller slettede
        orgunit_repo = Orgunit_repo(self.constr_lora)
        queue_repo = Queue_orgunit_repo(self.constr_lora)
        orgs_to_handle = orgunit_repo.get_orgunits('WHERE [updated] = 1 or [deleted] = 1 and [uuid] is not null')
        orgs_to_update = {}
        queue = {}
        i = 0
        for los_id in orgs_to_handle:
            org = orgs_to_handle[los_id]
            if org.updated == True and org.deleted == False:
                queue_item = Queue_orgunit(org.uuid, org.los_id, 'Updated', True)
                queue[i] = queue_item
                i+=1
                org.updated = False
                orgs_to_update[los_id] = org
            else:
                # hvis en orgunit er både uodated og deleted, vejer deleted tungere end updated
                queue_item = Queue_orgunit(org.uuid, org.los_id, 'Deleted', True)
                queue[i] = queue_item
                i+=1
                # nu hvor org er i køen som deleted, kan vi godt slette den fra orgunits, igen fordi deleted vejer tungere end updated
                orgunit_repo.delete_orgunit(los_id)
        orgunit_repo.update_orgunits(orgs_to_update)
        queue_repo.insert_queue_orgunits(queue)
    
        