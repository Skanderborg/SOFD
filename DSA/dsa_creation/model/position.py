class Position:
    def __init__(self, person_ref, opus_id, last_changed, position_title, position_short, los_id, paygrade_text, numerator, denominator, is_manager,
                 work_contract, work_contract_text, entry_date, leave_date, initial_date, entry_into_group):
        self.person_ref = person_ref
        self.opus_id = opus_id
        self.last_changed = last_changed
        self.position_title = position_title
        self.position_short = position_short
        self.los_id = los_id
        self.paygrade_text = paygrade_text
        self.numerator = numerator
        self.denominator = denominator
        self.is_manager = is_manager
        self.work_contract = work_contract
        self.work_contract_text = work_contract_text
        self.entry_date = entry_date
        self.leave_date = leave_date
        self.initial_date = initial_date
        self.entry_into_group = entry_into_group
