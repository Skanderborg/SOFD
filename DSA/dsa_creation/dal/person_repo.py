import pyodbc
from model.person import Person


class Person_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_persons(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM pyt.persons;")
        for row in cursor.fetchall():
            cpr = row[1]
            per = Person(cpr, row[2], row[3],
                         row[4], row[5], row[6], row[7])
            result[cpr] = per
        return result

    def insert_person(self, person):
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
