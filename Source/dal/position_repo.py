import pyodbc
from model.position import Position


class Position_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_positions(self, whereclause=None):
        if whereclause == None:
            whereclause = ""
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [opus_id], \
                                [uuid_userref], \
                                [los_id], \
                                [person_ref], \
                                [kmd_suppid], \
                                [title], \
                                [position_id], \
                                [title_short], \
                                [paygrade_title], \
                                [is_manager], \
                                [payment_method], \
                                [payment_method_text], \
                                [weekly_hours_numerator], \
                                [weekly_hours_denominator], \
                                [invoice_recipient], \
                                [pos_pnr], \
                                [dsuser], \
                                [start_date], \
                                [leave_date], \
                                [manager_opus_id], \
                                [manager_uuid_userref], \
                                [updated], \
                                [deleted], \
                                [ad_user_deleted] \
                        FROM [pyt].[positions] \
                        " + whereclause + ";")
        for row in cursor.fetchall():
            opus_id = row.opus_id
            pos = Position(opus_id, row.uuid_userref, row.los_id, row.person_ref, row.kmd_suppid, row.title,
                           row.position_id, row.title_short, row.paygrade_title, row.is_manager,
                           row.payment_method, row.payment_method_text, row.weekly_hours_numerator,
                           row.weekly_hours_denominator, row.invoice_recipient, row.pos_pnr, row.dsuser,
                           row.start_date, row.leave_date, row.manager_opus_id, row.manager_uuid_userref,
                           row.updated, row.deleted, row.ad_user_deleted)
            result[int(opus_id)] = pos
        return result

    def insert_positions(self, positions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in positions:
            position = positions[key]
            cursor.execute(
                "INSERT into [pyt].[positions]([opus_id], \
                                                [los_id], \
                                                [person_ref], \
                                                [kmd_suppid], \
                                                [title], \
                                                [title_short], \
                                                [position_id], \
                                                [paygrade_title], \
                                                [is_manager], \
                                                [payment_method], \
                                                [payment_method_text], \
                                                [weekly_hours_numerator], \
                                                [weekly_hours_denominator], \
                                                [invoice_recipient], \
                                                [pos_pnr], \
                                                [dsuser], \
                                                [start_date], \
                                                [leave_date], \
                                                [updated], \
                                                [deleted], \
                                                [ad_user_deleted]) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                position.opus_id,
                position.los_id,
                position.person_ref,
                position.kmd_suppid,
                position.position_title,
                position.position_title_short,
                position.position_id,
                position.position_paygrade_text,
                position.is_manager,
                position.payment_method,
                position.payment_method_text,
                position .weekly_hours_numerator,
                position.weekly_hours_denominator,
                position.invoice_recipient,
                position.pos_pnr,
                position.dsuser,
                position.start_date,
                position.leave_date,
                position.updated,
                position.deleted,
                position.ad_user_deleted)
        cnxn.commit()

    def update_positions(self, positions):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        for key in positions:
            position = positions[key]
            cursor.execute(
                "UPDATE [pyt].[positions] \
                SET [uuid_userref] = ?, \
                    [los_id] =?, \
                    [person_ref] = ?, \
                    [kmd_suppid] = ?, \
                    [title] = ?, \
                    [position_id] = ?, \
                    [title_short] = ?, \
                    [paygrade_title] = ?, \
                    [is_manager] = ?, \
                    [payment_method] = ?, \
                    [payment_method_text] = ?, \
                    [weekly_hours_numerator] = ?, \
                    [weekly_hours_denominator] = ?, \
                    [invoice_recipient] = ?, \
                    [pos_pnr] = ?, \
                    [dsuser] = ?, \
                    [start_date] = ?, \
                    [leave_date] = ?, \
                    [manager_opus_id] = ?, \
                    [manager_uuid_userref] = ?, \
                    [updated] = ?, \
                    [deleted] = ?, \
                    [ad_user_deleted] = ? \
                WHERE opus_id = ?",
                position.uuid_userref,
                position.los_id,
                position.person_ref,
                position.kmd_suppid,
                position.position_title,
                position.position_id,
                position.position_title_short,
                position.position_paygrade_text,
                position.is_manager,
                position.payment_method,
                position.payment_method_text,
                position.weekly_hours_numerator,
                position.weekly_hours_denominator,
                position.invoice_recipient,
                position.pos_pnr,
                position.dsuser,
                position.start_date,
                position.leave_date,
                position.manager_opus_id,
                position.manager_uuid_userref,
                position.updated,
                position.deleted,
                position.ad_user_deleted,
                position.opus_id)
        cnxn.commit()

    def delete_position(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "DELETE from [pyt].[positions] WHERE [opus_id] = ? ", opus_id)
        cnxn.commit()

    def get_disabled_orgunits(self):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT [los_id] FROM [pyt].[disabled_orgunits]")
        result = []
        for row in cursor.fetchall():
            result.append(row.los_id)
        return result
