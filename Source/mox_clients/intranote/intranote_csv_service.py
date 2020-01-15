import csv
from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from dal.users_repo import User_repo

class Intranote_csv_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def create_orgunit_csv(self):
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits('WHERE [deleted] = 0')
        with open('intranote_orgs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['los_id','name'])
            for los_id in orgs:
                org = orgs[los_id]
                writer.writerow([org.los_id,org.longname])

    def create_users_csv(self):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        poss = pos_repo.get_positions('WHERE [uuid_userref] is not NULL and [deleted] = 0')
        usrs = usr_repo.get_users()
        with open('intranote_usrs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['los_id','name'])
            for opus_id in poss:
                pos = poss[opus_id]
                usr = usrs[opus_id]
                writer.writerow([pos.position_title,usr.userid])