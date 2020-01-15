from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit

class Orgunit_queue_service:
    def __init__(self, constr_lora):
        self.orgunit_repo = Orgunit_repo(constr_lora)
        self.queue_repo = Queue_orgunit_repo(constr_lora)

    def create_orgunit_queue(self):
        orgs_to_handle = self.orgunit_repo.get_orgunits('WHERE [updated] = 1 or [deleted] = 1')
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
                org.deleted = False
                org.updated = False
                orgs_to_update[los_id] = org
        self.orgunit_repo.update_orgunits(orgs_to_update)
        self.queue_repo.insert_queue_orgunits(queue)
        
    def clean_orgunit_queue(self):
        queue_items_to_delete = self.queue_repo.get_orgunit_queueitems('WHERE [sts_org] = 1')
        for system_id in queue_items_to_delete:
            item = queue_items_to_delete[system_id]
            if item.change_type == "Deleted":
                self.orgunit_repo.delete_orgunit(item.los_id)
            self.queue_repo.delete_queue_orgunit(system_id)
        