from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from model.user import User
from model.position import Position

class User_position_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def 