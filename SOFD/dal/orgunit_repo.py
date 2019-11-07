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
        for row in cursor.fetchall():
            los_id = row[0]
            org = Orgunit(los_id, row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7], row[8], row[9], row[10], row[11],
                          row[12], row[13], row[14], row[15], row[16], row[17],
                          row[18], row[19], row[20], row[21], row[22])
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
