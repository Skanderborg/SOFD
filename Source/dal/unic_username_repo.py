import pyodbc
from model.unic_username import Unic_username

class Unic_username_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_unic_usernames(self, whereclause=None):
        if whereclause == None:
            whereclause = ""
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT [cpr], \
                    [unic_userid], \
                    [institution_nr], \
                    [opus_id] \
            FROM [unic].[unic_usernames] \
            " + whereclause + ";")
        for row in cursor.fetchall():
            unic_userid = row.unic_userid
            unic_username = Unic_username(row.cpr,
                                            unic_userid,
                                            row.institution_nr,
                                            row.opus_id)
            result[unic_userid] = unic_username
        return result

    def update_unic_usernames(self, unic_usernames):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in unic_usernames:
            unic_username = unic_usernames[key]
            cursor.execute("UPDATE [unic].[unic_usernames] \
                            SET [opus_id] = ? \
                            WHERE [unic_userid] = ?",
                           unic_username.opus_id,
                           unic_username.unic_userid)
        cnxn.commit()