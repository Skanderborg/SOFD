from model.user_queue import User_queue
import pydoc

class User_queue_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_user_queues(self, whereclause=None):
        if whereclause is None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [uuid], \
                                [opus_id], \
                                [change_type], \
                                [change_date] \
                        FROM [queue].[users] \
                        " + whereclause +";")
        for row in cursor.fetchall():
            uuid = row[0]
            usr_que = User_queue(uuid, row[1], row[2], row[3])
            result[uuid] = usr_que
        return result