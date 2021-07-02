from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from dal.sbsys_extension_repo import Sbsys_extension_repo
from model.sbsys_extension import Sbsys_extension

class Sbsys_extensions_service:
    def __init__(self, constr_lora, sbsys_extensionfield9, sbsys_extensionfield10):
        self.constr_lora = constr_lora
        self.sbsys_extensionfield9 = sbsys_extensionfield9
        self.sbsys_extensionfield10 = sbsys_extensionfield10

    def update_sbsys_extensions(self):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        sbsys_repo = Sbsys_extension_repo(self.constr_lora)
        usrs = usr_repo.get_users()
        poss = pos_repo.get_positions('WHERE uuid_userref IS NOT NULL and [ad_user_deleted] = 0')
        sbsys_extensions_full_list = {}

        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()

        for opus_id in poss:
            pos = poss[opus_id]
            usr = usrs[opus_id]
            # Der er åbentbart en risiko for at SamAccountnames, som er det der står i userID kan være helt forkete. Så vi laver lige et tjek.
            if len(usr.userid) != 6:
                continue
            # hvis løn har fucket op, kan der være medarbejdere uden orgunits.
            if pos.los_id not in orgs:
                continue
            sbsys_extensions_full_list[opus_id] = Sbsys_extensions_service.get_sbsys_extension(self, pos.los_id, opus_id, usr.userid)
        sbsys_extensions_to_insert = {}
        sbsys_extensions_to_update = {}
        sbsys_extensions_in_sofd = sbsys_repo.get_sbsys_extensions()

        for opus_id in sbsys_extensions_full_list:
            sbsys_extension_actual = sbsys_extensions_full_list[opus_id]
            if opus_id not in sbsys_extensions_in_sofd:
                sbsys_extensions_to_insert[opus_id] = sbsys_extension_actual
            else:
                sbsys_sofd = sbsys_extensions_in_sofd[opus_id]
                if sbsys_extension_actual != sbsys_sofd:
                    sbsys_extensions_to_update[opus_id] = sbsys_extension_actual
        sbsys_repo.insert_sbsys_extensions(sbsys_extensions_to_insert)
        sbsys_repo.update_sbsys_extensions(sbsys_extensions_to_update)

    # der skal muligvis mere med end opus_id og los
    def get_sbsys_extension(self, los_id, opus_id, userid):
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        user_org = orgs[los_id]
        
        sbsys_list = Sbsys_extensions_service.get_sbsys_extension_orgunits(self, user_org, orgs, [])
        last_org = len(sbsys_list) - 1
        sbsys_ext = Sbsys_extension(opus_id, userid)
        # test range
        for i in range(6):
            if i < last_org:
                sbsys_ext.add_extensionAttriute(sbsys_list[i])
            else:
                sbsys_ext.add_extensionAttriute(sbsys_list[last_org])
        return sbsys_ext
    
    def get_sbsys_extension_orgunits(self, org, orgs, res):
        if org.longname == 'Direktion1' or org.longname == 'Direktion2' or org.longname == 'Direktion3' or org.longname == 'Direktion4':
            org.longname = 'Direktion'
        res.append(org.longname)
        current_org = orgs[org.parent_orgunit_los_id]
        #if current_org.niveau > 4:
        #    res.append(org.longname)
        # OBS, direktion 1-4 (på niveau 4) og Borgmester (på niveau 2) skal sorteres fra, toppen af ORG strukturen ændre sig næsten aldrig
        # og fordi niveau 1-4 altid er de samme, springer vi dem faktisk bare helt over.
        # men hvis den gør, skal dette selvfølgelig opdateres - Carsten Møller er boss over det her og informeret
        # listen reverses før den returnes, så skanderborg kommune står først
        if current_org.niveau <= 4:
            res.append(self.sbsys_extensionfield10)
            res.append(self.sbsys_extensionfield9)
            return res[::-1]
        else:
            return Sbsys_extensions_service.get_sbsys_extension_orgunits(self, current_org, orgs, res)