import csv
from mox_clients.acubiz.acubiz_repo import Acubiz_repo
from dal.queue_users_repo import Queue_users_repo

class Acubiz_csv_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def create_users_csv(self, csv_file_path):
        repo = Acubiz_repo(self.constr_lora)
        queue_repo = Queue_users_repo(self.constr_lora)
        ams = repo.get_employees()
        queue = queue_repo.get_user_queues('WHERE mox_acubiz = 0')
        queue_items_to_update = {}
        with open(csv_file_path + 'Medarbejder.csv', 'w', newline='', encoding='iso-8859-1') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(['uuid',
                            'fullname',
                            'ad1',
                            'ad2',
                            'ad3',
                            'manager_uuid',
                            'email',
                            'los_id1_1',
                            'los_id1_2',
                            'los_id2_1',
                            'los_id2_2',
                            'cpr1',
                            'cpr2',
                            'nul',
                            'HomeEMS',
                            'Dim6',
                            'Dim7'])
            for opus_id in ams:
                am = ams[opus_id]
                deleted = '0'
                if am.deleted == True:
                    deleted = '1'
                writer.writerow([am.uuid_userref,
                                am.name,
                                am.userid,
                                am.userid,
                                am.userid,
                                am.manager_uuid_userref,
                                am.email,
                                am.los_id,
                                am.los_id,
                                str(am.los_id) + ' - ' + am.longname,
                                str(am.los_id) + ' - ' + am.longname,
                                am.person_ref,
                                am.person_ref,
                                deleted,
                                am.homeems,
                                am.dim6,
                                am.dim7])
                if opus_id in queue:
                    queue_item = queue[opus_id]
                    queue_item.mox_acubiz = True
                    queue_items_to_update[opus_id] = queue_item
        queue_repo.update_queue_users(queue_items_to_update)
