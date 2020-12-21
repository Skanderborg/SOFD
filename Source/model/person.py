class Person:
    def __init__(self, cpr, firstname, lastname, address, zipcode, city, country, updated, 
                display_firstname=None, display_lastname=None):
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
        self.display_firstname = display_firstname # probably needs to be one name if it's coming from displayname in ad
        self.display_lastname = display_lastname # probably needs to be one name if it's coming from displayname in ad

    def get_firstname_including_displayname(self):
        #print(self.display_lastname)
        if self.display_firstname == None:
            return self.firstname
        else:
            return self.display_firstname
            
    
    def get_lastname_including_displayname(self):
        if self.display_lastname == None:
            return self.lastname
        else:
            return self.display_lastname