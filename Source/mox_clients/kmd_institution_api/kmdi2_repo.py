import pyodbc

class Kmdl2_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_institutions_to_sync(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT [los_id], \
                        [kmdl2_id], \
                        [parent_orgunit_los_id], \
                        [kmdl2_name], \
                        [longname]\
                FROM [LORA_SOFD].[kmdl2].[v_institution_to_sync];")
            for row in cursor.fetchall():
                result[row.los_id] = {'los_id' : row.los_id, 'kmdi2_id' : row.kmdl2_id, 'parent_orgunit_los_id' : row.parent_orgunit_los_id,
                'longname' : row.longname}
        return result
    
    def get_dagtilbud(self):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "SELECT [los_id] \
                FROM [LORA_SOFD].[kmdl2].[dagtilbud];")
            for row in cursor.fetchall():
                result.append(row.los_id)
        return result

    def get_employees_in_orgunit(self, los_id):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "EXEC [kmdl2].[get_orgunit_employes] @los_id = ?;", los_id)
            for row in cursor.fetchall():
                result.append({'opus_id' : row.opus_id, 'firstname' : row.firstname, 'lastname' : row.lastname,
                'title' : row.title})
        return result

    def get_orgunit_and_children(self, los_id):
        result = []
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "EXEC [dbo].[get_all_orgunits_below] @Parent = ?;", los_id)
            for row in cursor.fetchall():
                result.append(str(row[0]))
        return result