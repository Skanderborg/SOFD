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
        queue_orgs = {}
        i = 0
        for los_id in updated_orgs:
            org = updated_orgs[los_id]
            if org.uuid != None:
                que_org = Queue_orgunit(org.uuid, org.los_id, 'Updated')
                queue_orgs[i] = que_org
                i += 1
            org.updated = False
            orgs_to_update[org.los_id] = org
        self.orgunit_repo.update_orgunits(orgs_to_update)
        self.queue_repo.insert_queue_orgunits(queue_orgs)