from dal.orgunit_repo import Orgunit_repo
from model.orgunit import Orgunit


class Orgunit_parent_uuid_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def set_parent_uuids(self):
        repo = Orgunit_repo(self.constr_lora)
        orgunits = repo.get_orgunits()
        for los_id in orgunits:
            orgunit = orgunits[los_id]
            parent_id = orgunit.parent_orgunit_los_id
            if parent_id in orgunits:
                parent = orgunits[parent_id]
                if orgunit.parent_orgunit_uuid == parent.uuid:
                    continue
                else:
                    orgunit.parent_orgunit_uuid = parent.uuid
                    repo.update_orgunit(orgunit)
