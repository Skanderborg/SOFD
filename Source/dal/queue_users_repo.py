from model.queue_user import Queue_user
import pyodbc


class Queue_users_repo:
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
                                [sts_org], \
                                [mox_acubiz] \
                        FROM [queue].[users_queue] \
                        " + whereclause + ";")
        for row in cursor.fetchall():
            usr_que = Queue_user(row.system_id, row.uuid, row.opus_id, row.change_type, row.sts_org, row.mox_acubiz)
            result[row.system_id] = usr_que
        return result

    def get_completed_user_queues(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [system_id], \
                                [uuid], \
                                [opus_id], \
                                [change_type], \
                                [sts_org], \
                                [mox_acubiz] \
                        FROM [queue].[users_queue] \
                        WHERE [sts_org] = 1 \
                            AND [mox_acubiz] = 1;")
        for row in cursor.fetchall():
            usr_que = Queue_user(row.system_id, row.uuid, row.opus_id, row.change_type, row.sts_org, row.mox_acubiz)
            result[row.system_id] = usr_que
        return result

    def insert_user_queue(self, queue_users):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in queue_users:
            queue_user = queue_users[key]
            cursor.execute(
                "INSERT INTO [queue].[users_queue]([uuid], \
                                             [opus_id], \
                                             [change_type], \
                                             [sts_org])  \
                VALUES (?, ?, ?, ?)",
                queue_user.uuid,
                queue_user.opus_id,
                queue_user.change_type,
                queue_user.sts_org)
        cnxn.commit()

    def update_queue_user(self, queue_user):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("UPDATE [queue].[users_queue] \
                        SET [uuid] = ?, \
                            [opus_id] = ?, \
                            [change_type] = ?, \
                            [sts_org] = ?, \
                            [mox_acubiz] = ? \
                            WHERE [system_id] = ?",
                        queue_user.uuid,
                        queue_user.opus_id,
                        queue_user.change_type,
                        queue_user.sts_org,
                        queue_user.mox_acubiz,
                        queue_user.system_id)
        cnxn.commit()

    def update_queue_users(self, queue_users):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for system_id in queue_users:
            user_queue = queue_users[system_id]
            cursor.execute("UPDATE [queue].[users_queue] \
                            SET [uuid] = ?, \
                                [opus_id] = ?, \
                                [change_type] = ?, \
                                [sts_org] = ?, \
                                [mox_acubiz] = ? \
                            WHERE [system_id] = ?",
                           user_queue.uuid,
                           user_queue.opus_id,
                           user_queue.change_type,
                           user_queue.sts_org,
                           user_queue.mox_acubiz,
                           system_id)
        cnxn.commit()

    def delete_person(self, system_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [queue].[users_queue] WHERE [system_id] = ? ", system_id)
        cnxn.commit()
