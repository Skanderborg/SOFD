import pyodbc
from model.person import Person


class Person_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_persons(self, whereclause=None):
        if whereclause == None:
            whereclause = ""
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
                    [country], \
                    [updated], \
                    [display_firstname], \
                    [display_lastname] \
            FROM [pyt].[persons] \
            " + whereclause + ";")
        for row in cursor.fetchall():
            cpr = row.cpr
            per = Person(cpr, row.firstname, row.lastname, row.address, row.zipcode, row.city, 
                            row.country, row.updated, row.display_firstname, row.display_lastname)
            result[cpr] = per
        return result

    def insert_persons(self, persons):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in persons:
            person = persons[key]
            cursor.execute(
                "INSERT INTO [pyt].[persons]([cpr], \
                                             [firstname], \
                                             [lastname], \
                                             [address], \
                                             [zipcode], \
                                             [city], \
                                             [country], \
                                             [updated], \
                                             [display_firstname], \
                                             [display_lastname]) \
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)",
                person.cpr,
                person.firstname,
                person.lastname,
                person.address,
                person.zipcode,
                person.city,
                person.country,
                person.display_firstname,
                person.display_lastname)
        cnxn.commit()

    def update_persons(self, persons):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in persons:
            person = persons[key]
            cursor.execute("UPDATE [pyt].[persons] \
                            SET [firstname] = ?, \
                                [lastname] = ?, \
                                [address] = ?, \
                                [zipcode] = ?, \
                                [city] = ?, \
                                [country] = ?, \
                                [updated] = ?, \
                                [display_firstname] = ?, \
                                [display_lastname] = ? \
                            WHERE [cpr] = ?",
                           person.firstname,
                           person.lastname,
                           person.address,
                           person.zipcode,
                           person.city,
                           person.country,
                           person.updated,
                           person.display_firstname,
                           person.display_lastname,
                           person.cpr)
        cnxn.commit()

    def delete_person(self, cpr):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [pyt].[persons] WHERE [cpr] = ?", cpr)
        cnxn.commit()
