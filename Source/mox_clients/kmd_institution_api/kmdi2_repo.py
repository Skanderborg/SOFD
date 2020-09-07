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
                result[row.los_id] = {'los_id' : row.los_id, 'kmdi2_id' : row.kmdl2_id, 'parent_orgunit_los_id' : row.parent_orgunit_los_id}
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

    def employees_in_tree(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        with cnxn:
            cursor = cnxn.cursor()
            cursor.execute(
                "EXEC [dbo].[get_all_orgunits_below] @Parent = 836771;")
            for row in cursor.fetchall():
                print(row)
        return result