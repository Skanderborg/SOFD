import pyodbc
from model.orgunit import Orgunit


class Orgunit_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_orgunits(self, whereclause=None):
        if whereclause == None:
            whereclause = ""

        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [los_id], \
                               [uuid], \
                               [last_changed], \
                               [longname], \
                               [startdate], \
                               [enddate], \
                               [parent_orgunit_los_id], \
                               [shortname], \
                               [street], \
                               [zipcode], \
                               [city], \
                               [phonenumber], \
                               [cvr], \
                               [ean], \
                               [seNr], \
                               [pnr], \
                               [orgtype], \
                               [orgtypetxt], \
                               [manager_opus_id], \
                               [hierarchy], \
                               [niveau], \
                               [area], \
                               [costcenter] \
                        FROM [pyt].[Orgunits] \
                        " + whereclause + ";")
        rows = cursor.fetchall()
        for row in rows:
            los_id = row.los_id
            org = Orgunit(los_id, row.uuid, row.last_changed, row.longname, row.startdate,
                          row.enddate, row.parent_orgunit_los_id, row.shortname, row.street,
                          row.zipcode, row.city, row.phonenumber, row.cvr, row.ean, row.seNr,
                          row.pnr, row.orgtype, row.orgtypetxt, row.manager_opus_id,
                          row.hierarchy, row.niveau, row.area, row.costcenter)
            result[int(los_id)] = org
        return result

    def insert_orgunit(self, orgunit):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "INSERT INTO [pyt].[Orgunits]([los_id], \
                                       [last_changed], \
                                       [longname], \
                                       [startdate], \
                                       [enddate], \
                                       [parent_orgunit_los_id], \
                                       [shortname], \
                                       [street], \
                                       [zipcode], \
                                       [city], \
                                       [phonenumber], \
                                       [cvr], \
                                       [ean], \
                                       [seNr], \
                                       [pnr], \
                                       [orgtype], \
                                       [orgtypetxt], \
                                       [costcenter], \
                                       [hierarchy], \
                                       [niveau], \
                                       [area], \
                                       [new], \
                                       [updated], \
                                       [deleted]) \
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0)",
            orgunit.los_id,
            orgunit.last_changed,
            orgunit.longname,
            orgunit.startdate,
            orgunit.enddate,
            orgunit.parent_orgunit_los_id,
            orgunit.shortname,
            orgunit.street,
            orgunit.zipcode,
            orgunit.city,
            orgunit.phonenumber,
            orgunit.cvr,
            orgunit.ean,
            orgunit.seNr,
            orgunit.pnr,
            orgunit.orgtype,
            orgunit.orgtypetxt,
            orgunit.costcenter,
            orgunit.hierarchy,
            orgunit.niveau,
            orgunit.area)
        cnxn.commit()

    def update_orgunit(self, orgunit):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "UPDATE [pyt].[Orgunits] \
            SET [los_id] = ?, \
                [uuid] = ?, \
                [last_changed] = ?, \
                [longname] = ?, \
                [startdate] = ?, \
                [enddate] = ?, \
                [parent_orgunit_los_id] = ?, \
                [shortname] = ?, \
                [street] = ?, \
                [zipcode] = ?, \
                [city] = ?, \
                [phonenumber] = ?, \
                [cvr] = ?, \
                [ean] = ?, \
                [seNr] = ?, \
                [pnr] = ?, \
                [orgtype] = ?, \
                [orgtypetxt] = ?, \
                [costcenter] = ?, \
                [manager_opus_id] = ?, \
                [hierarchy] = ?, \
                [niveau] = ?, \
                [area] = ?, \
                [updated] = 1 \
            WHERE [los_id] = ?",
            orgunit.los_id,
            orgunit.uuid,
            orgunit.last_changed,
            orgunit.longname,
            orgunit.startdate,
            orgunit.enddate,
            orgunit.parent_orgunit_los_id,
            orgunit.shortname,
            orgunit.street,
            orgunit.zipcode,
            orgunit.city,
            orgunit.phonenumber,
            orgunit.cvr,
            orgunit.ean,
            orgunit.seNr,
            orgunit.pnr,
            orgunit.orgtype,
            orgunit.orgtypetxt,
            orgunit.costcenter,
            orgunit.manager_opus_id,
            orgunit.hierarchy,
            orgunit.niveau,
            orgunit.area,
            orgunit.los_id)
        cnxn.commit()

    def delete_orgunit(self, los_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "UPDATE [pyt].[Orgunits] SET [deleted] = 1 WHERE [los_id] = ? ", los_id)
        cnxn.commit()
