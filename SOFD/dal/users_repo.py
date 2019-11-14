from model.user import User
import pyodbc


class User_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_users(self, whereclause=None):
        if whereclause is None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [Opus_id], \
                                [Uuid], \
                                [UserId], \
                                [Email], \
                                [Phone], \
                                [Updated], \
                                [WorkMobile], \
                                [Deleted_in_ad] \
                        FROM [dbo].[Users] \
                        " + whereclause + ";")
        for row in cursor.fetchall():
            opus_id = row.Opus_id
            usr = User(opus_id, row.Uuid, row.UserId, row.Email, row.Phone, row.Updated,
                       row.WorkMobile, row.Deleted_in_ad)
            result[int(opus_id)] = usr
        return result
