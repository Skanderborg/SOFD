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
                    [extensionAttribute10], \
                    [extensionAttribute11], \
                    [extensionAttribute12], \
                    [extensionAttribute13], \
                    [extensionAttribute14] \
            FROM [sbsys].[extensionattributes] \
            " + whereclause + ";")
        for row in cursor.fetchall():
            opus_id = row.opus_id
            ext = Sbsys_extension(opus_id)
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
            cursor.execute(
                "INSERT INTO [sbsys].[extensionattributes]([opus_id], \
                                            [extensionAttribute10], \
                                            [extensionAttribute11], \
                                            [extensionAttribute12], \
                                            [extensionAttribute13], \
                                            [extensionAttribute14] \
                VALUES (?, ?, ?, ?, ?)",
                ext.opus_id,
                ext.extensionattributes[0],
                ext.extensionattributes[1],
                ext.extensionattributes[2],
                ext.extensionattributes[3],
                ext.extensionattributes[4])
        cnxn.commit()

    def update_sbsys_extensions(self, sbsys_extensions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in sbsys_extensions:
            ext = sbsys_extensions[key]
            cursor.execute("UPDATE [sbsys].[extensionattributes] \
                            SET [extensionAttribute10] = ?, \
                                [extensionAttribute11] = ?, \
                                [extensionAttribute12] = ?, \
                                [extensionAttribute13] = ?, \
                                [extensionAttribute14] = ? \
                            WHERE [opus_id] = ?",
                           person.extensionattributes[0],
                           person.extensionattributes[1],
                           person.extensionattributes[2],
                           person.extensionattributes[3],
                           person.extensionattributes[4],
                           person.opus_id)
        cnxn.commit()

    def delete_sbsys_extensions(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE FROM [sbsys].[extensionattributes] WHERE [opus_id] = ?", cpr)
        cnxn.commit()
