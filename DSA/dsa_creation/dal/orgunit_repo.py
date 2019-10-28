import pyodbc
from model.orgunit import Orgunit


class Orgunit_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_orgunits(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM pyt.orgunits;")
        for row in cursor.fetchall():
            los_id = row[1]
            org = Orgunit(los_id, row[2], row[3], row[4], row[5], row[6],
                          row[7], row[8], row[9], row[10], row[11], row[12],
                          row[13], row[14], row[15], row[16], row[17])
            result[los_id] = org
        return result
