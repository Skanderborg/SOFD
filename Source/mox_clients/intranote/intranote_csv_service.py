import csv
from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo
from dal.users_repo import User_repo
from dal.person_repo import Person_repo
from dal.unic_username_repo import Unic_username_repo
from model.unic_username import Unic_username

class Intranote_csv_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def create_orgunit_csv(self, csv_file_path):
        org_repo = Orgunit_repo(self.constr_lora)
        orgs = org_repo.get_orgunits('WHERE [deleted] = 0')
        with open(csv_file_path + 'Orgenhed.csv', 'w', newline='', encoding='UTF-16LE') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['los_id','uuid','last_changed','longname','startdate','enddate','parent_orgunit_los_id',
                                'parent_orgunit_uuid','shortname', 'street', 'zipcode','city','phonenumber','cvr',
                                'ean','manager_opus_id'])
            for los_id in orgs:
                org = orgs[los_id]
                writer.writerow([org.los_id, org.uuid, org.last_changed, org.longname, org.startdate, org.enddate,
                                    org.parent_orgunit_los_id, org.parent_orgunit_uuid, org.shortname, org.street,
                                    org.zipcode, org.city, org.phonenumber, org.cvr, org.ean, org.manager_opus_id])

    def create_users_csv(self, csv_file_path):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        per_repo = Person_repo(self.constr_lora)
        poss = pos_repo.get_positions('WHERE [uuid_userref] is not NULL and [deleted] = 0')
        usrs = usr_repo.get_users()
        pers = per_repo.get_persons()
        with open(csv_file_path + 'Medarbejder.csv', 'w', newline='', encoding='UTF-16LE') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['cpr','firstname','lastname','opus_id','uuid_userref','los_id','title','is_manager','start_date',
                                'leave_date','manager_opus_id','Uuid','UserId','Email','Phone','WorkMobile'])
            for opus_id in poss:
                pos = poss[opus_id]
                usr = usrs[opus_id]
                per = pers[pos.person_ref]
                writer.writerow([pos.person_ref, per.firstname, per.lastname, opus_id, pos.uuid_userref, pos.los_id, pos.position_title,
                                    pos.is_manager, pos.start_date, pos.leave_date, pos.manager_opus_id, pos.uuid_userref, usr.userid,
                                    usr.email, usr.phone, usr.workmobile])

    def create_unic_csv(self, csv_file_path):
        unic_repo = Unic_username_repo(self.constr_lora)
        unics = unic_repo.get_unic_usernames('WHERE [opus_id] is not null')
        with open(csv_file_path + 'Unilogin.csv', 'w', newline='', encoding='UTF-16LE') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['cpr','unilogin'])
            for unilogin in unics:
                unic = unics[unilogin]
                writer.writerow([unic.cpr, unilogin])