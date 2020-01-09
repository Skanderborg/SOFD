class Unic_username:
    def __init__(self, cpr, unic_userid, institution_nr, opus_id):
        self.cpr = cpr
        self.unic_userid = unic_userid
        self.institution_nr = int(institution_nr)
        self.opus_id = opus_id