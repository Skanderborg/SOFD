from dal.orgunit_repo import Orgunit_repo
from dal.org_uuid_repo import Org_uuid_repo
from model.orgunit import Orgunit


class Orgunit_uuid_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def set_orgunit_uuid(self):
        # opsætter UUID'er på organisations enehder, der kommer fra OPUS XML'en som endnu ikke har et UUID
        orgs_to_update = {}
        uuid_repo = Org_uuid_repo(self.constr_lora)
        org_repo = Orgunit_repo(self.constr_lora)
        uuids = uuid_repo.get_org_uuids()
        orgs = org_repo.get_orgunits(
            "WHERE [uuid] is null and [hierarchy] = 'opus'")
        for los_id in orgs:
            if los_id in uuids:
                org = orgs[los_id]
                org.uuid = uuids[los_id]
                org.updated = True
                orgs_to_update[los_id] = org
        org_repo.update_orgunits(orgs_to_update)

    def set_parent_uuids(self):
        # Tjekker parent UUID på organisations enheder, og opdaterer det hvis der er lavet forandringer.
        orgs_to_update = {}
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
                    orgunit.updated = True
                    orgs_to_update[los_id] = orgunit
        repo.update_orgunits(orgs_to_update)
