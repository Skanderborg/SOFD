import pyodbc


class Unic_institution_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_institutions(self, whereclause=None):
        if whereclause is None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [institution_nr], \
                                [los_id] \
                        FROM [unic].[institutions] \
                        " + whereclause + ";")
        for row in cursor.fetchall():
            result[int(row.institution_nr)] = int(row.los_id)
        return result