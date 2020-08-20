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
                        [los_id] \
                FROM [LORA_SOFD].[kmdl2].[employees_in_tree];")
            for row in cursor.fetchall():
                result[row.opus_id] = row.los_id
        return result

'''
SELECT [system_id]
      ,[los_id]
  FROM [LORA_SOFD].[kmdl2].[dagtilbud]


SELECT [system_id]
      ,[los_id]
      ,[kmdl2_id]
      ,[kmdl2_name]
      ,[longname]
  FROM [LORA_SOFD].[kmdl2].[institution_ids]

SELECT [los_id]
      ,[longname]
      ,[parent_orgunit_los_id]
  FROM [LORA_SOFD].[kmdl2].[institution_tree]
'''