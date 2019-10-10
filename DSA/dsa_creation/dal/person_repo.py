import pyodbc


class Person_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def Get_persons(self):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM pyt.persons;")
        for row in cursor.fetchall():
            print(row)
        # return {}

    def Insert_person(self, person):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "INSERT into pyt.persons(cpr, firstname, lastname, address, zipcode, city, country) VALUES (?, ?, ?, ?, ?, ?, ?)",
            person.cpr,
            person.firstname,
            person.lastname,
            person.address,
            person.zipcode,
            person.city,
            person.country)
        cnxn.commit()
