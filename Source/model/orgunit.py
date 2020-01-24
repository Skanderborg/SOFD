import datetime


class Orgunit:
    def __init__(self, los_id, uuid, last_changed, longname, startdate, enddate,
                 parent_orgunit_los_id, parent_orgunit_uuid, shortname, street, zipcode, city,
                 phonenumber, cvr, ean, seNr, pnr, orgtype, orgtypetxt, manager_opus_id, hierarchy,
                 niveau,  area, updated, deleted, costcenter=None):
        self.los_id = los_id
        self.uuid = uuid
        self.last_changed = last_changed
        self.longname = longname
        if startdate != None:
            self.startdate = str(startdate)
        else:
            self.startdate = str(datetime.datetime(1900, 1, 1))
        if enddate != None:
            self.enddate = str(enddate)
        else:
            self.enddate = enddate
        if parent_orgunit_los_id is None:
            parent_orgunit_los_id = 0
        self.parent_orgunit_los_id = int(parent_orgunit_los_id)
        self.parent_orgunit_uuid = parent_orgunit_uuid
        self.shortname = shortname
        self.street = street
        self.zipcode = zipcode
        self.city = city
        if phonenumber != None:
            self.phonenumber = phonenumber
        else:
            self.phonenumber = '87947000'
        self.cvr = cvr
        self.ean = ean
        self.seNr = seNr
        self.pnr = pnr
        self.orgtype = int(orgtype)
        self.orgtypetxt = orgtypetxt
        self.manager_opus_id = manager_opus_id
        self.hierarchy = hierarchy
        self.niveau = niveau
        self.area = area
        self.costcenter = costcenter
        self.updated = updated in ['true', 'True', 1]
        self.deleted = deleted in ['true', 'True', 1]
