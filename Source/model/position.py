class Position:
    def __init__(self, opus_id, uuid_userref, los_id, person_ref, kmd_suppid, position_title, position_id,
                 position_title_short, position_paygrade_text, is_manager, payment_method, payment_method_text,
                 weekly_hours_numerator, weekly_hours_denominator, invoice_recipient, pos_pnr, dsuser,
                 start_date, leave_date, manager_opus_id, manager_uuid_userref, updated, deleted, ad_user_deleted):
        self.opus_id = int(opus_id)
        self.uuid_userref = uuid_userref
        self.los_id = int(los_id)
        self.person_ref = person_ref
        self.kmd_suppid = int(kmd_suppid)
        self.position_title = position_title
        self.position_id = int(position_id)
        if position_title_short == None:
            position_title_short = "Ingen position title short"
        self.position_title_short = position_title_short
        if position_paygrade_text == None:
            position_paygrade_text = "Ingen paygrade title"
        self.position_paygrade_text = position_paygrade_text
        self.is_manager = is_manager in ['true', 'True', 1]
        self.payment_method = payment_method
        self.payment_method_text = payment_method_text
        self.weekly_hours_numerator = float(weekly_hours_numerator)
        self.weekly_hours_denominator = float(weekly_hours_denominator)
        self.invoice_recipient = invoice_recipient in ['true', 'True', 1]
        self.pos_pnr = pos_pnr
        self.dsuser = dsuser
        self.start_date = str(start_date)
        if leave_date != None:
            self.leave_date = str(leave_date)
        else:
            self.leave_date = leave_date
        if manager_opus_id != None:
            self.manager_opus_id = int(manager_opus_id)
        else:
            self.manager_opus_id = None
        self.manager_uuid_userref = manager_uuid_userref
        self.updated = updated in ['true', 'True', 1]
        self.deleted = deleted in ['true', 'True', 1]
        self.ad_user_deleted = ad_user_deleted in ['true', 'True', 1]
