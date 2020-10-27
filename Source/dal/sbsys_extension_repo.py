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
            cursor.execute("INSERT INTO [sbsys].[sbsysusers_orgs]([opus_id], \
                                                        [userid], \
                                                        [extensionAttribute9], \
                                                        [extensionAttribute10], \
                                                        [extensionAttribute11], \
                                                        [extensionAttribute12], \
                                                        [extensionAttribute13], \
                                                        [extensionAttribute14], \
                                                        [updated]) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)",
                ext.opus_id,
                ext.userid,
                ext.extensionAttributes[0],
                ext.extensionAttributes[1],
                ext.extensionAttributes[2],
                ext.extensionAttributes[3],
                ext.extensionAttributes[4],
                ext.extensionAttributes[5])
            cnxn.commit()

    def update_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            cursor.execute("UPDATE [sbsys].[sbsysusers_orgs] \
                            SET [extensionAttribute9] = ?, \
                                [extensionAttribute10] = ?, \
                                [extensionAttribute11] = ?, \
                                [extensionAttribute12] = ?, \
                                [extensionAttribute13] = ?, \
                                [extensionAttribute14] = ?, \
                                [updated] = 1 \
                            WHERE [opus_id] = ?",
                            ext.extensionAttributes[0],
                            ext.extensionAttributes[1],
                            ext.extensionAttributes[2],
                            ext.extensionAttributes[3],
                            ext.extensionAttributes[4],
                            ext.extensionAttributes[5],
                            ext.opus_id)
        cnxn.commit()

    def delete_sbsys_extensions(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [sbsys].[extensionattributes] WHERE [opus_id] = ?", opus_id)
        cnxn.commit()
