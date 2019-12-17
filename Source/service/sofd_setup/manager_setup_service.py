from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo


class Manager_setup_service:
    def __init__(self, constr_lora):
        self.org_repo = Orgunit_repo(constr_lora)
        self.pos_repo = Position_repo(constr_lora)
        self.orgs = None

    def set_orgunit_manager(self):
        orgs = self.org_repo.get_orgunits()
        managers = self.pos_repo.get_positions('WHERE [is_manager] = 1')
        orgs_to_update = {}
        for mkey in managers:
            manager = managers[mkey]
            org = orgs[manager.los_id]
            if org.manager_opus_id == manager.opus_id:
                continue
            else:
                org.manager_opus_id = manager.opus_id
                org.updated = True
                orgs_to_update[org.los_id] = org
        self.org_repo.update_orgunits(orgs_to_update)

    def set_nearest_manager(self):
        self.orgs = self.org_repo.get_orgunits()
        positions = self.pos_repo.get_positions()
        positions_to_update = {}

        for pkey in positions:
            position = positions[pkey]
            manager_id = Manager_setup_service.get_manager(
                self, position.los_id)
            manager_uuid = positions[manager_id].uuid_userref
            if position.manager_opus_id != manager_id or position.manager_uuid_userref != manager_uuid:
                position.manager_opus_id = manager_id
                position.manager_uuid_userref = manager_uuid
                position.updated = True
                positions_to_update[pkey] = position
            else:
                continue
        self.pos_repo.update_positions(positions_to_update)

    def get_manager(self, los_id):
        orgunit = self.orgs[los_id]
        if orgunit.manager_opus_id != None:
            return orgunit.manager_opus_id
        else:
            return Manager_setup_service.get_manager(self,  orgunit.parent_orgunit_los_id)
