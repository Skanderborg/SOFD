import pyodbc
from model.person import Person


class Person_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_persons(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT [cpr], \
                    [firstname], \
                    [lastname], \
                    [address], \
                    [zipcode], \
                    [city], \
                    [country] \
            FROM [pyt].[persons] \
            WHERE [deleted] = 0;")
        for row in cursor.fetchall():
            cpr = row[0]
            per = Person(cpr, row[1], row[2],
                         row[3], row[4], row[5], row[6])
            result[cpr] = per
        return result

    def insert_person(self, person):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "INSERT INTO [pyt].[persons]([cpr], \
                                         [firstname], \
                                         [lastname], \
                                         [address], \
                                         [zipcode], \
                                         [city], \
                                         [country], \
                                         [updated], \
                                         [deleted])  \
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, 0)",
            person.cpr,
            person.firstname,
            person.lastname,
            person.address,
            person.zipcode,
            person.city,
            person.country)
        cnxn.commit()

    def update_person(self, person):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("UPDATE [pyt].[persons] \
                        SET [firstname] = ?, \
                             lastname = ?, \
                             address = ?, \
                             zipcode = ?, \
                             city = ?, \
                             country = ?, \
                             updated = 1, \
                        WHERE cpr = ? ",
                       person.firstname,
                       person.lastname,
                       person.address,
                       person.zipcode,
                       person.city,
                       person.country,
                       person.cpr)
        cnxn.commit()

    def delete_person(self, cpr):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "UPDATE [pyt].[persons] SET [deleted] = 1 WHERE [cpr] = ? ", cpr)
        cnxn.commit()
