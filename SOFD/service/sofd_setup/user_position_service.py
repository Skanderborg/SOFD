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
        positions = pos_repo.get_positions("WHERE uuid_userref is null")
        users = usr_repo.get_users()
        for key in positions:
            if key in users:
                position = positions[key]
                user = users[key]
                position.uuid_userref = user.uuid
                pos_repo.update_position(position)
