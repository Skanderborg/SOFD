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

    def bind_unic_to_position(self):
        unic_repo = Unic_username_repo(self.constr_lora)
        unic_list = unic_repo.get_unic_usernames('WHERE opus_id is NULL')
        pos_repo = Position_repo(self.constr_lora)
        unics_to_update = {}
        for unic_userid in unic_list:
            unic = unic_list[unic_userid]
            positions_related_to_cpr = pos_repo.get_positions("WHERE person_ref = '%s'" % unic.cpr)
            pos_amount = len(positions_related_to_cpr)
            if pos_amount == 1:
                unic.opus_id = positions_related_to_cpr[0].opus_id
                unics_to_update[unic_userid] = unic
            elif pos_amount > 1:
                los_id_to_match = self.institutions[unic.institution_nr]
                best_guess_for_match_position = None
                for los_id in positions_related_to_cpr:
                    pos = positions_related_to_cpr[los_id]
                    if Unic_to_position_service.is_unic_username_and_position_match(self, pos.los_id, los_id_to_match):
                        if best_guess_for_match_position == None:
                            best_guess_for_match_position = pos
                        else:
                            if best_guess_for_match_position.weekly_hours_numerator < pos.weekly_hours_numerator:
                                best_guess_for_match_position = pos
                unic.opus_id = pos.opus_id
                unics_to_update[unic_userid] = unic
            else:
                continue
        unic_repo.update_unic_usernames(unics_to_update)
            
    '''
        repo = Unic_username_repo(self.constr_lora)
        unic_usernames = repo.get_unic_usernames('WHERE opus_id is NULL')
        unic_usernames = {}
        for unic_userid in unic_usernames:
            unic_username = unic_usernames[unic_userid]
            username_positions = []
            for opus_id in self.positions:
                pos = self.positions[opus_id]
                if pos.person_ref == unic_username.cpr:
                    username_positions.append(pos)
            if len(username_positions) == 1:
                # hvis der kun er en stilling som passer til CPR nummeret på et unic username, bliver der et match.
                # det betyder at der godt kan kobles flere unic brugernavne på en stilling - men dette sker kun når de er på flere institutioner, og bør sorteres fra på anden vis
                unic_username.opus_id = username_positions[0].opus_id
                usernames_to_update[unic_userid] = unic_username
            else:
                # Når der er flere stillinger som kan matche et unic brugernavn, forsøger vi at matche en stilling som passer.
                # Er der flere end én eller ingen, der matcher, så opretter vi ingen forbindelse
                los_id_to_match = self.institutions[unic_username.institution_nr]
                match_pos = None
                match_count = 0
                for pos in username_positions:
                    if Unic_to_position_service.is_unic_username_and_position_match(self, pos.los_id, los_id_to_match):
                        match_pos = pos
                        match_count +=1
                if match_count == 1:
                    username.opus_id = match_pos.opus_id
                    usernames_to_update[unic_userid] = username
                elif match_count > 1:
                    x = 1
                else:
                    continue
        repo.update_unic_usernames(usernames_to_update)
    '''
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