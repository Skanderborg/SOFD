from model.sbsys_extension import Sbsys_extension
import pyodbc



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
                    [extensionAttribute9], \
                    [extensionAttribute10], \
                    [extensionAttribute11], \
                    [extensionAttribute12], \
                    [extensionAttribute13], \
                    [extensionAttribute14] \
            FROM [sbsys].[sbsysusers_orgs] \
            " + whereclause + ";")
        for row in cursor.fetchall():
            opus_id = row.opus_id
            ext = Sbsys_extension(opus_id, row.userid)
            ext.add_extensionAttriute(row.extensionAttribute9)
            ext.add_extensionAttriute(row.extensionAttribute10)
            ext.add_extensionAttriute(row.extensionAttribute11)
            ext.add_extensionAttriute(row.extensionAttribute12)
            ext.add_extensionAttriute(row.extensionAttribute13)
            ext.add_extensionAttriute(row.extensionAttribute14)
            result[opus_id] = ext
        return result

    def insert_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            ext9 = ext.extensionAttributes[0]
            ext10 = ext.extensionAttributes[1]
            ext11 = ext.extensionAttributes[2]
            ext12 = ext.extensionAttributes[3]
            ext13 = ext.extensionAttributes[4]
            ext14 = ext.extensionAttributes[5]
            cursor.execute(
                "INSERT INTO [sbsys].[sbsysusers_orgs]([opus_id], \
                                                        [userid], \
                                                        [extensionAttribute9], \
                                                        [extensionAttribute10], \
                                                        [extensionAttribute11], \
                                                        [extensionAttribute12], \
                                                        [extensionAttribute13], \
                                                        [extensionAttribute14]) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ext.opus_id,
                ext.userid,
                ext9,
                ext10,
                ext11,
                ext12,
                ext13,
                ext14)
        cnxn.commit()

    def update_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            ext9 = ext.extensionAttributes[0]
            ext10 = ext.extensionAttributes[1]
            ext11 = ext.extensionAttributes[2]
            ext12 = ext.extensionAttributes[3]
            ext13 = ext.extensionAttributes[4]
            ext14 = ext.extensionAttributes[5]
            cursor.execute("UPDATE [sbsys].[sbsysusers_orgs] \
                            SET [extensionAttribute9] = ?, \
                                [extensionAttribute10] = ?, \
                                [extensionAttribute11] = ?, \
                                [extensionAttribute12] = ?, \
                                [extensionAttribute13] = ?, \
                                [extensionAttribute14] = ? \
                            WHERE [opus_id] = ?",
                            ext9,
                            ext10,
                            ext11,
                            ext12,
                            ext13,
                            ext14,
                            ext.opus_id)
        cnxn.commit()

    def delete_sbsys_extensions(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [sbsys].[extensionattributes] WHERE [opus_id] = ?", opus_id)
        cnxn.commit()
