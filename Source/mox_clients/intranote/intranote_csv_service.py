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
        with open('orgs.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["los_id","name"])
            for los_id in orgs:
                org = orgs[los_id]
                writer.writerow([org.los_id,org.longname])
