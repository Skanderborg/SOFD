import pyodbc
from model.queue_orgunit import Queue_orgunit

class Queue_orgunit_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_orgunit_queueitems(self, whereclause=None):
        if whereclause is None:
            whereclause = ""
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT  [system_id], \
                                [uuid], \
                                [los_id], \
                                [change_type] \
                        FROM [queue].[orgunit_queue]\
                        " + whereclause + ";")
        for row in cursor.fetchall():
            org_que = Queue_orgunit(row.uuid, row.los_id, row.change_type, row.system_id)
            result[row.system_id] = org_que
        return result

    def insert_queue_orgunits(self, queue_orgunits):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in queue_orgunits:
            org = queue_orgunits[key]
            cursor.execute(
                "INSERT INTO [queue].[orgunit_queue]([uuid], \
                                                    [los_id], \
                                                    [change_type]) \
                VALUES (?, ?, ?)",
                org.uuid,
                org.los_id,
                org.change_type)
        cnxn.commit()

    def update_queue_orgunits(self, org_ques):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for system_id in org_ques:
            org_que = org_ques[system_id]
            cursor.execute("UPDATE [queue].[orgunit_queue] \
                            SET [uuid] = ?, \
                                [los_id] = ?, \
                                [change_type] = ?, \
                                [sts_org] = ? \
                            WHERE [system_id] = ?",
                           org_que.uuid,
                           org_que.los_id,
                           org_que.change_type,
                           org_que.sts_org,
                           system_id)
        cnxn.commit()

    def delete_queue_orgunit(self, system_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [queue].[orgunit_queue] WHERE [system_id] = ? ", system_id)
        cnxn.commit()

