import pyodbc
from model.position import Position


class Position_repo:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_positions(self):
        result = {}
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM pyt.positions;")
        for row in cursor.fetchall():
            opus_id = row[1]
            pos = Position(opus_id, row[2], row[3], row[4], row[5], row[6],
                           row[7], row[8], row[9], row[10], row[11], row[12],
                           row[13], row[14], row[15], row[16], row[17])
            result[opus_id] = pos
        return result

    def insert_position(self, position):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "INSERT into pyt.positions(opus_id, los_id, person_ref, title, title_short, position_id, paygrade_title, is_manager, \
                                     payment_method, payment_method_text, weekly_hours_numerator, weekly_hours_denominator, \
                                     invoice_recipient, pos_pnr, dsuser, start_date, leave_date, updated, deleted\
                                         )  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 0)",
            position.opus_id,
            position.los_id,
            position.person_ref,
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
            position.leave_date)
        cnxn.commit()

    def update_position(self, position):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "UPDATE pyt.positions SET los_id = ?, person_ref = ?, title = ?, title_short = ?, position_id = ?, \
                                      paygrade_title = ?, is_manager = ?, payment_method = ?, payment_method_text = ?, \
                                      weekly_hours_numerator = ?, weekly_hours_denominator = ?, invoice_recipient = ?, \
                                          pos_pnr = ?, dsuser = ?, start_date = ?, leave_date = ?, updated = 1 WHERE opus_id = ?",
            position.los_id,
            position.person_ref,
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
            position.opus_id)
        cnxn.commit()

    def delete_position(self, opus_id):
        cnxn = pyodbc.connect(self.constr_lora)
        cursor = cnxn.cursor()
        cursor.execute(
            "UPDATE pyt.positions SET deleted = 1 WHERE opus_id = ? ", opus_id)
        cnxn.commit()
