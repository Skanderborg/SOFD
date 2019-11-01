from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo


class Manager_setup_service:
    def __init__(self, constr_lora):
        self.org_repo = Orgunit_repo(constr_lora)
        self.pos_repo = Position_repo(constr_lora)

    def set_orgunit_manager(self):
        orgs = self.org_repo.get_orgunits()
        managers = self.pos_repo.get_positions('WHERE [is_manager] = 1')

        for mkey in managers:
            manager = managers[mkey]
            org = orgs[manager.los_id]
            if org.manager_opus_id == manager.opus_id:
                continue
            else:
                org.manager_opus_id = manager.opus_id
                org_repo.update_orgunit(org)

    def set_nearest_manager(self):
        org_repo = Orgunit_repo(self.constr_lora)
        pos_repo = Position_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        positions = pos_repo.get_positions()

        for pkey in positions:
            x = 1

    def get_manager(self, los_id):
        orgunit = self.org_repo.get_orgunits('WHERE [los_id] = ' + los_id)[0]
        if orgunit.manager_opus_id != None:
            return orgunit.manager_opus_id
        else:
            return get_manager(orgunit.parent_orgunit_los_id)
