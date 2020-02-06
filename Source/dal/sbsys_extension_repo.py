import pyodbc
from model.sbsys_extension import Sbsys_extension


class Sbsys_extension_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_sbsys_extensions(self, whereclause=None):
        if whereclause == None:
            whereclause = ""
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "SELECT [opus_id], \
                    [userid], \
                    [los_id_9], \
                    [extensionAttribute9], \
                    [los_id_10], \
                    [extensionAttribute10], \
                    [los_id_11], \
                    [extensionAttribute11], \
                    [los_id_12], \
                    [extensionAttribute12], \
                    [los_id_13], \
                    [extensionAttribute13], \
                    [los_id_14], \
                    [extensionAttribute14] \
            FROM [sbsys].[sbsysusers_orgs] \
            " + whereclause + ";")
        for row in cursor.fetchall():
            opus_id = row.opus_id
            ext = Sbsys_extension(opus_id, row.userid)
            ext.add_extensionAttriute(row.los_id_9, row.extensionAttribute9)
            ext.add_extensionAttriute(row.los_id_10, row.extensionAttribute10)
            ext.add_extensionAttriute(row.los_id_11, row.extensionAttribute11)
            ext.add_extensionAttriute(row.los_id_12, row.extensionAttribute12)
            ext.add_extensionAttriute(row.los_id_13, row.extensionAttribute13)
            ext.add_extensionAttriute(row.los_id_14, row.extensionAttribute14)
            result[opus_id] = ext
        return result

    def insert_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            cursor.execute(
                "INSERT INTO [sbsys].[sbsysusers_orgs]([opus_id], \
                                                        [userid], \
                                                        [los_id_9], \
                                                        [extensionAttribute9], \
                                                        [los_id_10], \
                                                        [extensionAttribute10], \
                                                        [los_id_11], \
                                                        [extensionAttribute11], \
                                                        [los_id_12], \
                                                        [extensionAttribute12], \
                                                        [los_id_13], \
                                                        [extensionAttribute13], \
                                                        [los_id_14], \
                                                        [extensionAttribute14] \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ext.opus_id,
                ext.userid,
                ext.extensionattributes[0][0],
                ext.extensionattributes[0][1],
                ext.extensionattributes[1][0],
                ext.extensionattributes[1][1],
                ext.extensionattributes[2][0],
                ext.extensionattributes[2][1],
                ext.extensionattributes[3][0],
                ext.extensionattributes[3][1],
                ext.extensionattributes[4][0],
                ext.extensionattributes[4][1],
                ext.extensionattributes[5][0],
                ext.extensionattributes[5][1])
        cnxn.commit()

    def update_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            cursor.execute("UPDATE [sbsys].[sbsysusers_orgs] \
                            SET [los_id_9] = ?, \
                                [extensionAttribute9] = ?, \
                                [los_id_10] = ?, \
                                [extensionAttribute10] = ?, \
                                [los_id_11] = ?, \
                                [extensionAttribute11] = ?, \
                                [los_id_12] = ?, \
                                [extensionAttribute12] = ?, \
                                [los_id_13] = ?, \
                                [extensionAttribute13] = ?, \
                                [los_id_14] = ?, \
                                [extensionAttribute14] = ? \
                            WHERE [opus_id] = ?",
                            ext.extensionattributes[0][0],
                            ext.extensionattributes[0][1],
                            ext.extensionattributes[1][0],
                            ext.extensionattributes[1][1],
                            ext.extensionattributes[2][0],
                            ext.extensionattributes[2][1],
                            ext.extensionattributes[3][0],
                            ext.extensionattributes[3][1],
                            ext.extensionattributes[4][0],
                            ext.extensionattributes[4][1],
                            ext.extensionattributes[5][0],
                            ext.extensionattributes[5][1],
                            ext.opus_id)
        cnxn.commit()

    def delete_sbsys_extensions(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [sbsys].[extensionattributes] WHERE [opus_id] = ?", opus_id)
        cnxn.commit()
