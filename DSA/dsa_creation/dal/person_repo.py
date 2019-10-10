import pyodbc


class Person_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def Get_persons(self):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM [LORA_SOFD].[dbo].[Persons];")
        row = cursor.fetchone()
        while row:
            print(row)
            row = cursor.fetchone()
        # return {}
