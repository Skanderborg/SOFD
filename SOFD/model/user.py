class User:
    def __init__(self, opus_id, uuid, userid, email, phone, updated, workmobile, deleted_in_ad):
        self.opus_id = opus_id
        self.uuid = uuid
        self.userid = userid
        self.email = email
        self.phone = phone
        self.updated = updated in ['true', 'True', 1]
        self.mobile = mobile
        self.deleteD_in_ad = deleted_in_ad in ['true', 'True', 1]
