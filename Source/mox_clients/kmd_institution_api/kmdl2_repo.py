import pyodbc

class kmdl2_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def employees_in_tree(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT [opus_id], \
                        [los_id];")
            for row in cursor.fetchall():
                result[row.opus_id] = row.los_id
        return result
