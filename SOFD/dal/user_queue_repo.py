from model.user_queue import User_queue
import pyodbc


class User_queue_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_user_queues(self, whereclause=None):
        if whereclause is None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [system_id], \
                                [uuid], \
                                [opus_id], \
                                [change_type], \
                                [change_date] \
                        FROM [queue].[users] \
                        " + whereclause + ";")
        for row in cursor.fetchall():
            system_id = row[0]
            usr_que = User_queue(system_id, row[1], row[2], row[3], row[4])
            result[system_id] = usr_que
        return result

    def insert_user_queue(self, usr_que):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "INSERT INTO [queue].[users]([uuid], \
                                         [opus_id], \
                                         [change_type], \
                                         [change_date])  \
            VALUES (?, ?, ?, ?)",
            usr_que.uuid,
            usr_que.opus_id,
            usr_que.change_type,
            usr_que.change_date)
        cnxn.commit()

    def delete_person(self, system_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [queue].[users] WHERE [system_id] = ? ", system_id)
        cnxn.commit()
