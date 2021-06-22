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
        pos_repo = Position_repo(self.constr_lora)
        los_ids_to_ignore = pos_repo.get_disabled_orgunits()
        orgs = org_repo.get_orgunits('WHERE [deleted] = 0')
        with open(csv_file_path + 'Orgenhed.csv', 'w', newline='', encoding='iso-8859-1') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['los_id','uuid','last_changed','longname','startdate','enddate','parent_orgunit_los_id',
                                'parent_orgunit_uuid','shortname', 'street', 'zipcode','city','phonenumber','cvr',
                                'ean','manager_opus_id'])
            for los_id in orgs:
                if los_id in los_ids_to_ignore:
                    continue
                org = orgs[los_id]
                writer.writerow([org.los_id, org.uuid, org.last_changed, org.longname, org.startdate, org.enddate,
                                    org.parent_orgunit_los_id, org.parent_orgunit_uuid, org.shortname, org.street,
                                    org.zipcode, org.city, org.phonenumber, org.cvr, org.ean, org.manager_opus_id])

    def create_users_csv(self, csv_file_path):
        pos_repo = Position_repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)
        per_repo = Person_repo(self.constr_lora)
        poss = pos_repo.get_positions('WHERE [deleted] = 0 and [ad_user_deleted] = 0')
        usrs = usr_repo.get_users()
        pers = per_repo.get_persons()
        los_ids_to_ignore = pos_repo.get_disabled_orgunits()

        # OBS!!! det her skal være klogere
        tmp_cpr = []

        # NYYYYYYYYYYYYYYT
        # tja, lærerne skal åbentbart med alligevel duuuu
        unic_cprs = []
        unic_repo = Unic_username_repo(self.constr_lora)
        unics = unic_repo.get_unic_usernames('WHERE [opus_id] is not null')
        for unilogin in unics:
                unic = unics[unilogin]
                unic_cprs.append(unic.cpr)

        cvs_ready_positions = []
        for opus_id in poss:
            pos = poss[opus_id]
            if pos.los_id in los_ids_to_ignore:
                continue

            cpr = pos.person_ref

            #OBS SKAL FORBEDRES
            #if cpr in tmp_cpr or pos.uuid_userref == None:
                #continue

            if cpr in tmp_cpr:
                continue
            if pos.uuid_userref == None and cpr not in unic_cprs:
                continue

            per = pers[cpr]
            usr_userid = None
            usr_email = None
            usr_phone = None
            usr_workmobile = None
            if pos.uuid_userref != None:
                usr = usrs[opus_id]
                usr_userid = usr.userid
                usr_email = usr.email
                usr_phone = usr.phone
                usr_workmobile = usr.workmobile
        
            cvs_ready_positions.append([pos.person_ref, per.firstname, per.lastname, opus_id, pos.uuid_userref, pos.los_id, pos.position_title,
                                    pos.is_manager, pos.start_date, pos.leave_date, pos.manager_opus_id, pos.uuid_userref, usr_userid,
                                    usr_email, usr_phone, usr_workmobile])
            #OBS skal forbedres
            tmp_cpr.append(cpr)

            with open(csv_file_path + 'Medarbejder.csv', 'w', newline='', encoding='iso-8859-1') as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(['cpr','firstname','lastname','opus_id','uuid_userref','los_id','title','is_manager','start_date',
                                'leave_date','manager_opus_id','Uuid','UserId','Email','Phone','WorkMobile'])
                for position in cvs_ready_positions:
                    writer.writerow(position)



        '''

        with open(csv_file_path + 'Medarbejder.csv', 'w', newline='', encoding='iso-8859-1') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['cpr','firstname','lastname','opus_id','uuid_userref','los_id','title','is_manager','start_date',
                                'leave_date','manager_opus_id','Uuid','UserId','Email','Phone','WorkMobile'])
            for opus_id in poss:
                pos = poss[opus_id]
                if pos.los_id in los_ids_to_ignore:
                    continue

                per = pers[pos.person_ref]
                usr_userid = None
                usr_email = None
                usr_phone = None
                usr_workmobile = None
                if pos.uuid_userref != None:
                    usr = usrs[opus_id]
                    usr_userid = usr.userid
                    usr_email = usr.email
                    usr_phone = usr.phone
                    usr_workmobile = usr.workmobile

            
                
                writer.writerow([pos.person_ref, per.firstname, per.lastname, opus_id, pos.uuid_userref, pos.los_id, pos.position_title,
                                    pos.is_manager, pos.start_date, pos.leave_date, pos.manager_opus_id, pos.uuid_userref, usr_userid,
                                    usr_email, usr_phone, usr_workmobile])
            '''
    def create_unic_csv(self, csv_file_path):
        unic_repo = Unic_username_repo(self.constr_lora)
        unics = unic_repo.get_unic_usernames('WHERE [opus_id] is not null')
        with open(csv_file_path + 'Unilogin.csv', 'w', newline='', encoding='iso-8859-1') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['cpr','unilogin'])
            for unilogin in unics:
                unic = unics[unilogin]
                writer.writerow([unic.cpr, unilogin])



'''
Kan vi sorterer på unic brugerne, og evt. så der ikke kommer flere af dem der har flere ansættelser?
Vi kan genbruge noget af logikken fra KMDI2 snitfladen, som også gætter stillinger.

Skal brugere som ikke har en ad/unic med? - Det kommer der en mail.



'''