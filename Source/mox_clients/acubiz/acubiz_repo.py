import pyodbc
from mox_clients.acubiz.acubiz_model import Acubiz_model


class Acubiz_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_employees(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        #[unic_userid], \
        cursor.execute(
            "SELECT [uuid_userref], \
                    [firstname], \
                    [lastname], \
                    [UserId], \
                    [Email], \
                    [los_id], \
                    [person_ref], \
                    [manager_uuid_userref], \
                    [longname], \
                    [deleted], \
                    [opus_id] \
            FROM [acubiz].[acubiz_to_csv] \
            WHERE [manager_uuid_userref] is not null and [uuid_userref];")# is not null or [unic_userid] is not null;")
        for row in cursor.fetchall():
            am = Acubiz_model(row.uuid_userref,
                                row.firstname,
                                row.lastname,
                                row.UserId,
                                row.Email,
                                row.los_id,
                                row.person_ref,
                                row.manager_uuid_userref,
                                row.longname,
                                None,
                                #row.unic_userid,
                                row.deleted,
                                row.opus_id,
                                self.get_HomeEMS(row.los_id),
                                self.get_dim6(row.los_id),
                                self.get_dim7(row.los_id))
            result[int(row.opus_id)] = am
        return result

    def get_kodning(self):
        res = {}
        res[1047964] = 'Boenhed Bavnebjerg'
        res[834291] = 'Boenhed Bavnebjerg'
        res[844322] = 'Boenhed Bavnebjerg'
        res[844323] = 'Boenhed Bavnebjerg'
        res[849266] = 'Boenhed 02'
        res[849267] = 'Boenhed 18'
        res[849268] = 'Boenhed 04'
        res[849269] = 'Boenhed 08'
        res[849270] = 'Boenhed 42'
        res[849271] = 'Boenhed 12'
        res[849272] = 'Boenhed 40'
        res[849273] = 'Boenhed 16'
        res[849274] = 'Boenhed 10'
        res[849275] = 'Boenhed 14'
        res[849276] = 'Boenhed 20'
        res[863745] = 'Boenhed Bavnebjerg'
        res[871237] = 'Boenhed 44'
        res[872577] = 'Boenhed 06'
        return res

    def get_HomeEMS(self, los_id):
        dim7list = self.get_kodning()
        if los_id in dim7list:
            return 'SkanderborgSocialomraade'
        else:
            return 'GOLM-B4XQTY'

    def get_dim6(self, los_id):
        dim7list = self.get_kodning()
        if los_id in dim7list:
            return 'Sølund'
        else:
            return ''

    def get_dim7(self, los_id):
        dim7list = self.get_kodning()
        if los_id in dim7list:
            return dim7list[los_id]
        else:
            return ''