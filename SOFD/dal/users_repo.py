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
            opus_id = row[0]
            usr = User(opus_id, row[1], row[2], row[3], row[4], row[5],
                        row[6], row[7])
            result[int(opus_id)] = usr
        return result
