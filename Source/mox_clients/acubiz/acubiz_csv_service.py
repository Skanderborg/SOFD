import csv
from mox_clients.acubiz.acubiz_repo import Acubiz_repo

class Acubiz_csv_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def create_users_csv(self, csv_file_path):
        repo = Acubiz_repo(self.constr_lora)
        ams = repo.get_employees()
        with open(csv_file_path + 'Medarbejder.csv', 'w', newline='', encoding='iso-8859-1') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['uuid',
                            'fullname',
                            'ad1',
                            'ad2',
                            'ad3',
                            'manager_uuid',
                            'email',
                            'cost_center',
                            'los_id1',
                            'los_id2',
                            'cpr1',
                            'cpr2',
                            'nul',])
            for key in ams:
                am = ams[key]
                writer.writerow([am.uuid_userref,
                                am.name,
                                am.userid,
                                am.userid,
                                am.userid,
                                am.manager_uuid_userref,
                                am.email,
                                am.costcenter,
                                am.los_id,
                                str(am.los_id) + ' - ' + am.longname,
                                am.person_ref,
                                am.person_ref,
                                '0'])
