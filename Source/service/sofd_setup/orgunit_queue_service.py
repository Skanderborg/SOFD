from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit

class Orgunit_queue_service:
    def __init__(self, constr_lora):
        self.orgunit_repo = Orgunit_repo(constr_lora)
        self.queue_repo = Queue_orgunit_repo(constr_lora)

    def run_orgunit_queue_setup(self):
        updated_orgs = self.orgunit_repo.get_orgunits('WHERE [updated] = 1')
        deleted_orgs = self.orgunit_repo.get_orgunits('WHERE [deleted] = 1')
        orgs_to_update = {}
        i=0
        queue_orgs = {}
        for los_id in updated_orgs:
            # hvis org både er updated og deleted:
            if los_id in deleted_orgs:
                continue
            else:
                org = updated_orgs[los_id]
                if org.uuid != None:
                    que_org = Queue_orgunit(org.uuid, org.los_id, 'Updated')
                    queue_orgs[i] = que_org
                    i+=1
                org.updated = False
                orgs_to_update[org.los_id] = org
        for los_id in deleted_orgs:
            org = deleted_orgs[los_id]
            que_org = Queue_orgunit(org.uuid, org.los_id, 'Deleted')
            queue_orgs[i] = que_org
            i+=1
            org.deleted = False
        self.orgunit_repo.update_orgunits(orgs_to_update)
        self.queue_repo.insert_queue_orgunits(queue_orgs)
        
    def clean_orgunit_queue(self):
        queue_items_to_delete = self.queue_repo.get_orgunit_queueitems('WHERE [sts_org] = 1')
        for system_id in queue_items_to_delete:
            item = queue_items_to_delete[system_id]
            if item.change_type == "Deleted":
                self.orgunit_repo.delete_orgunit(item.los_id)
            self.queue_repo.delete_queue_orgunit(system_id)
        