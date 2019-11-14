import pyodbc


class Org_uuid_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_org_uuids(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [OrgOpusID], \
                               [orguuid] \
                        FROM [ad].[org_uiid];")
        for row in cursor.fetchall():
            result[int(row.OrgOpusID)] = row.orguuid
        return result
