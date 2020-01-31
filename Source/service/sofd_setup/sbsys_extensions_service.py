from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from model.sbsys_extension import Sbsys_extension

class Sbsys_extensions_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def setup_sbsys_extensions(self):
        pos_repo = Position_repo(self.constr_lora)
        
        poss = pos_repo.get_positions('WHERE uuid_userref IS NOT NULL')
        for opus_id in poss:
            pos = poss[opus_id]
            Sbsys_extensions_service.create_sbsys_extension_thing(self, pos.los_id, opus_id)

    # der skal muligvis mere med end opus_id og los
    def create_sbsys_extension_thing(self, los_id, opus_id):
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        user_org = orgs[los_id]
        sbsys_list = Sbsys_extensions_service.get_sbsys_orgunits(user_org, orgs, [])
        last_org = len(sbsys_list) - 1
        sbsys_ext = Sbsys_extension()
        # test range
        for i in range(5):
            if i < last_org:
                sbsys_ext.add_extensionAttriute(sbsys_list[i])
            else:
                sbsys_ext.add_extensionAttriute(sbsys_list[last_org])


    def get_sbsys_orgunits(self, org, orgs, res):
        res.append(org.longname)
        current_org = orgs[org.parent_orgunit_los_id]
        # OBS, direktion 1-3 skal sorteres fra, derfor skal vi fange niveau her og jeg kan ikke huske det
        # i hovedet
        if current_org.niveau == 4:
            current_org = orgs[org.parent_orgunit_los_id]
            Sbsys_extensions_service.get_sbsys_orgunits(self, current_org, orgs, res)
        elif current_org.longname == 'Direktion':
            return res.reverse()
        else:
            Sbsys_extensions_service.get_sbsys_orgunits(self, current_org, orgs, res)

