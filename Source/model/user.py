class User:
    def __init__(self, opus_id, uuid, userid, email, phone, updated, workmobile):
        self.opus_id = opus_id
        self.uuid = uuid
        self.userid = userid
        self.email = email
        self.phone = phone
        self.updated = updated in ['true', 'True', 1]
        self.workmobile = workmobile
