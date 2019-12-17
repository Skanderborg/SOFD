from dal.orgunit_repo import Orgunit_repo
from dal.queue_orgunit_repo import Queue_orgunit_repo
from model.queue_orgunit import Queue_orgunit
from model.orgunit import Orgunit
from service.email_service import Email_service

class Orgunit_queue_service:
    def __init__(self, constr_lora):
        self.orgunit_repo = Orgunit_repo(constr_lora)
        self.queue_repo = Queue_orgunit_repo(constr_lora)

    def run_orgunit_queue_setup(self, email_service):
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
            elif org.updated == False and org.deleted == True:
                queue_item = Queue_orgunit(org.uuid, org.los_id, 'Deleted', True)
                queue[i] = queue_item
                i+=1
                org.deleted = False
                orgs_to_update[los_id] = org
            else:
                email_service.send_mail('jacob.aagaard.bennike@skanderborg.dk', 'SOFD Error: orgunit_queue.py', 'Orgunit er både opdateret og slettet los_id: ' + los_id)
                continue
        self.orgunit_repo.update_orgunits(orgs_to_update)
        self.queue_repo.update_queue_orgunits(queue)
        
    def clean_orgunit_queue(self):
        queue_items_to_delete = self.queue_repo.get_orgunit_queueitems('WHERE [sts_org] = 1')
        for system_id in queue_items_to_delete:
            item = queue_items_to_delete[system_id]
            if item.change_type == "Deleted":
                self.orgunit_repo.delete_orgunit(item.los_id)
            self.queue_repo.delete_queue_orgunit(system_id)
        