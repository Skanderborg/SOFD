from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from model.user import User
from model.position import Position


class User_position_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def link_user_to_position(self):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        positions = pos_repo.get_positions()
        users = usr_repo.get_users()
        positions_to_update = {}
        for key in positions:
            position = positions[key]
            if key in users:
                user = users[key]
                if position.uuid_userref == None or position.uuid_userref != user.uuid:
                    position.uuid_userref = user.uuid
                    positions_to_update[key] = position
            else:
                if position.uuid_userref != None:
                    position.uuid_userref = None
                    positions_to_update[key] = position

        pos_repo.update_positions(positions_to_update)
