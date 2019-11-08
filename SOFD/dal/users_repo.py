from model.user import User
import pydoc

class User_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_users(self, whereclause=None):
        if whereclause is None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [opus_id], \
                                [uuid], \
                                [samaccount], \
                                [email], \
                                [phone], \
                                [mobile] \
                        FROM [dbo].[users] \
                        " + whereclause +";")
        for row in cursor.fetchall():
            opus_id = row[0]
            usr = User(opus_id, row[1], row[2], row[3], row[4], row[5])
            result[int(opus_id)] = usr
        return result