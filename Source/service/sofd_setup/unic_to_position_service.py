from dal.orgunit_repo import Orgunit_repo
from dal.unic_institution_repo import Unic_institution_repo
from dal.unic_username_repo import Unic_username_repo
from model.unic_username import Unic_username
from model.orgunit import Orgunit

class Unic_to_position_service:
    def __init__(self, lora_constr):
        self.lora_constr = lora_constr