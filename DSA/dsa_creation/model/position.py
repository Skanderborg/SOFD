class Position:
    def __init__(self, opus_id, los_id, person_ref, position_title, position_id, position_title_short,
                 position_paygrade_text, is_manager, payment_method, payment_method_text,
                 weekly_hours_numerator, weekly_hours_denominator, invoice_recipient, pos_pnr, dsuser,
                 entry_date, leave_date, initial_date, entry_into_group, last_changed):
        self.opus_id = opus_id
        self.los_id = los_id
        self.person_ref = person_ref
        self.position_title = position_title
        self.position_id = position_id
        self.position_title_short = position_title_short
        self.position_paygrade_text = position_paygrade_text
        self.is_manager = is_manager
        self.payment_method = payment_method
        self.payment_method_text = payment_method_text
        self.weekly_hours_numerator = weekly_hours_numerator
        self.weekly_hours_denominator = weekly_hours_denominator
        self.invoice_recipient = invoice_recipient
        self.pos_pnr = pos_pnr
        self.dsuser = dsuser
        self.entry_date = entry_date
        self.leave_date = leave_date
        self.initial_date = initial_date
        self.entry_into_group = entry_into_group
        self.last_changed = last_changed
