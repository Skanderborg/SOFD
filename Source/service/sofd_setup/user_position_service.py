from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from model.user import User
from model.position import Position


class User_position_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def link_user_to_position(self):
        '''
        Funktion der kobler positions, hvis data kommer fra fra OPUS løn og personale
        med users, hvis data kommer fra AD.
        Hvis der er en AD bruger med OPUS ID, kan der oprettes forbindelse mellem de to.
        Ligeledes, hvis der har været en forbindelse, som ikke er der længere, skal linket mellem de to fjernes.

        IT har et redskab hvor de kan flytte opus_id på brugere, derfor skal vi også tjekke om opus_id på position og user stemmer over ens.
        '''
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        positions = pos_repo.get_positions()
        users = usr_repo.get_users()
        positions_to_update = {}
        for opus_id in positions:
            position = positions[opus_id]
            if opus_id in users:
                user = users[opus_id]
                if position.uuid_userref == None or position.uuid_userref != user.uuid or position.opus_id != user.opus_id:
                    position.uuid_userref = user.uuid
                    position.updated = True
                    positions_to_update[opus_id] = position
            else:
                if position.uuid_userref != None:
                    # hvis brugeren ikke findes i dbo.users, betyder det at ad_brugeren er slettet fra position, i såfald skal brugere i "slettes køen" med uuid før uuid fjernes.
                    position.ad_user_deleted = True
                    positions_to_update[opus_id] = position

        pos_repo.update_positions(positions_to_update)
