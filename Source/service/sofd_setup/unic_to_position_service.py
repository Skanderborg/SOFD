from dal.orgunit_repo import Orgunit_repo
from dal.unic_institution_repo import Unic_institution_repo
from dal.unic_username_repo import Unic_username_repo
from dal.position_repo import Position_repo
from model.position import Position
from model.unic_username import Unic_username
from model.orgunit import Orgunit

class Unic_to_position_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora
        org_repo = Orgunit_repo(constr_lora)
        pos_repo = Position_repo(constr_lora)
        unic_institution_repo = Unic_institution_repo(constr_lora)
        self.orgunits = org_repo.get_orgunits()
        self.positions = pos_repo.get_positions()
        self.institutions = unic_institution_repo.get_institutions()

    def blackmagic(self):
        repo = Unic_username_repo(self.constr_lora)
        usernames = repo.get_unic_usernames('WHERE opus_id is NULL')
        usernames_to_update = {}
        for unic_userid in usernames:
            username = usernames[unic_userid]
            username_positions = []
            for opus_id in self.positions:
                pos = self.positions[opus_id]
                if pos.person_ref == username.cpr:
                    username_positions.append(pos)
            if len(username_positions) == 1:
                # hvis der kun er en stilling som passer til CPR nummeret på et unic username, bliver der et match.
                # det betyder at der godt kan kobles flere unic brugernavne på en stilling - men dette sker kun når de er på flere institutioner, og bør sorteres fra på anden vis
                username.opus_id = username_positions[0].opus_id
                usernames_to_update[unic_userid] = username
            else:
                # Når der er flere stillinger som kan matche et unic brugernavn, forsøger vi at matche en stilling som passer.
                # Er der flere end én eller ingen, der matcher, så opretter vi ingen forbindelse
                los_id_to_match = self.institutions[username.institution_nr]
                match_pos = None
                match_count = 0
                for pos in username_positions:
                    if Unic_to_position_service.is_unic_username_and_position_match(self, pos.los_id, los_id_to_match):
                        match_pos = pos
                        match_count +=1
                if match_count == 1:
                    username.opus_id = match_pos.opus_id
                    usernames_to_update[unic_userid] = username
                else:
                    continue
        repo.update_unic_usernames(usernames_to_update)

    def is_unic_username_and_position_match(self, current_los_id, los_id_to_match):
        orgunit = self.orgunits[current_los_id]
        if orgunit.parent_orgunit_los_id == 0:
            return False
        elif orgunit.los_id == los_id_to_match:
            return True
        else:
            return Unic_to_position_service.is_unic_username_and_position_match(self, orgunit.parent_orgunit_los_id, los_id_to_match)


    '''
    hvis der er flere end et match:

    '''