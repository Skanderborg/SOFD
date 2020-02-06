from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from model.sbsys_extension import Sbsys_extension

class Sbsys_extensions_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def setup_sbsys_extensions(self):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        usrs = usr_repo.get_users()
        poss = pos_repo.get_positions('WHERE uuid_userref IS NOT NULL')
        sbsys_extensions_full_list = []
        for opus_id in poss:
            pos = poss[opus_id]
            usr = usrs[opus_id]
            sbsys_extensions_full_list.append(Sbsys_extensions_service.create_sbsys_extension_thing(self, pos.los_id, opus_id, usr.userid))
        print(len(sbsys_extensions_full_list))

    # der skal muligvis mere med end opus_id og los
    def create_sbsys_extension_thing(self, los_id, opus_id, userid):
        print(los_id, opus_id, userid)
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        user_org = orgs[los_id]
        
        sbsys_list = Sbsys_extensions_service.get_sbsys_orgunits(self, user_org, orgs, [])
        print(sbsys_list)
        last_org = len(sbsys_list) - 1
        sbsys_ext = Sbsys_extension(opus_id, userid)
        # test range
        for i in range(5):
            if i < last_org:
                sbsys_ext.add_extensionAttriute(sbsys_list[i][0], sbsys_list[i][1])
            else:
                sbsys_ext.add_extensionAttriute(sbsys_list[last_org][0], sbsys_list[last_org][1])
        return sbsys_ext
    
    def get_sbsys_orgunits(self, org, orgs, res):
        res.append([org.los_id, org.longname])
        current_org = orgs[org.parent_orgunit_los_id]
        # OBS, direktion 1-3 (på niveau 4) og Borgmester (på niveau 2) skal sorteres fra, toppen af ORG strukturen ændre sig næsten aldrig
        # men hvis den gør, skal dette selvfølgelig opdateres - Carsten Møller er boss over det her og informeret
        # tænker ikke
        if current_org.niveau == 4:
            current_org = orgs[current_org.parent_orgunit_los_id]
        if current_org.niveau == 2:
            current_org = orgs[current_org.parent_orgunit_los_id]

        if current_org.longname == 'Skanderborg Kommune':
            res.append([current_org.los_id, current_org.longname])
            return res[::-1]
        else:
            return Sbsys_extensions_service.get_sbsys_orgunits(self, current_org, orgs, res)
