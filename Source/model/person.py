class Person:
    def __init__(self, cpr, firstname, lastname, address, zipcode, city, country, updated, displayname):
        self.cpr = cpr
        if firstname == None:
            firstname = 'Intet navn'
        self.firstname = firstname
        if lastname == None:
            lastname = 'Intet navn'
        self.lastname = lastname
        if address == None:
            address = 'Ingen addresse'
        self.address = address
        if zipcode == None:
            zipcode = 'Intet postnr'
        self.zipcode = zipcode
        if city == None:
            city = 'Ingen by'
        self.city = city
        if country == None:
            country = 'Intet'
        self.country = country
        self.updated = updated in ['true', 'True', 1]
        self.displayname = displayname
