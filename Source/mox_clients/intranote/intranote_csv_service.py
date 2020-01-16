import csv
from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from dal.person_repo import Person_repo

class Intranote_csv_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def create_orgunit_csv(self, csv_file_path):
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits('WHERE [deleted] = 0')
        with open(csv_file_path + 'intranote_orgs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['orgunit_id','name','parent_orgunit_id'])
            for los_id in orgs:
                org = orgs[los_id]
                writer.writerow([org.los_id,org.longname,org.parent_orgunit_los_id])

    def create_users_csv(self, csv_file_path):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        per_repo = Person_repo(self.constr_lora)
        poss = pos_repo.get_positions('WHERE [uuid_userref] is not NULL and [deleted] = 0')
        usrs = usr_repo.get_users()
        pers = per_repo.get_persons()
        with open(csv_file_path + 'intranote_usrs.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['position_title','orgunit_id','ad_samaccount','email'])
            for opus_id in poss:
                pos = poss[opus_id]
                usr = usrs[opus_id]
                per = pers[pos.person_ref]
                writer.writerow([pos.position_title,pos.los_id,usr.userid,usr.email])