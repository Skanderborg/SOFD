import pyodbc
from mox_clients.acubiz.acubiz_model import Acubiz_model


class Acubiz_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_employees(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT [uuid_userref], \
                    [firstname], \
                    [lastname], \
                    [UserId], \
                    [Email], \
                    [costcenter], \
                    [los_id], \
                    [person_ref], \
                    [manager_uuid_userref], \
                    [longname], \
                    [unic_userid], \
                    [deleted], \
                    [opus_id] \
            FROM [acubiz].[acubiz_to_csv] \
            WHERE [manager_uuid_userref] is not null and [uuid_userref] is not null or [unic_userid] is not null;")
        for row in cursor.fetchall():
            am = Acubiz_model(row.uuid_userref,
                                row.firstname,
                                row.lastname,
                                row.UserId,
                                row.Email,
                                row.costcenter, 
                                row.los_id,
                                row.person_ref,
                                row.manager_uuid_userref,
                                row.longname,
                                row.unic_userid,
                                row.deleted,
                                row.opus_id)
            result[int(row.opus_id)] = am
        return result