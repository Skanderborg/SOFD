class Orgunit:
    def __init__(self, los_id, last_changed, longname, startdate, enddate, 
                parent_org_unit, shortname, street, zipcode, city, phonenumber, cvr, 
                ean, seNr, pnr, costcenter, orgtype, orgtypetxt):
        self.los_id = los_id
        self.last_changed = last_changed
        self.longname = longname
        self.startdate = startdate
        self.enddate = enddate
        self.parent_org_unit = parent_org_unit
        self.shortname = shortname
        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.phonenumber = phonenumber
        self.cvr = cvr
        self.ean = ean
        self.seNr = seNr
        self.pnr = pnr
        self.costcenter = costcenter
        self.orgtype = orgtype
        self.orgtypetxt = orgtypetxt
