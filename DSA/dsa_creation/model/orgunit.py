class Orgunit:
    def __init__(self, los_id, last_changed, longname, startdate, enddate,
                 parent_orgunit_los_id, shortname, street, zipcode, city, phonenumber, cvr,
                 ean, seNr, pnr, orgtype, orgtypetxt, costcenter=None):
        self.los_id = los_id
        self.last_changed = last_changed
        self.longname = longname
        self.startdate = startdate
        self.enddate = enddate
        self.parent_orgunit_los_id = parent_orgunit_los_id
        self.shortname = shortname
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.phonenumber = phonenumber
        self.cvr = cvr
        self.ean = ean
        self.seNr = seNr
        self.pnr = pnr
        self.orgtype = orgtype
        self.orgtypetxt = orgtypetxt
        self.costcenter = costcenter
