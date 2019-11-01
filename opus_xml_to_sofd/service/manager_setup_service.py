from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo


class Manager_setup_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def set_orgunit_manager(self):
        org_repo = Orgunit_repo(self.constr_lora)
        pos_repo = Position_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        managers = pos_repo.get_positions('WHERE [is_manager] = 1')

        for mkey in managers:
            manager = managers[mkey]
            org = orgs[manager.los_id]
            if org.manager_opus_id == manager.opus_id:
                continue
            else:
                org.manager_opus_id = manager.opus_id
                org_repo.update_orgunit(org)

    def set_nearest_manager(self):
        
