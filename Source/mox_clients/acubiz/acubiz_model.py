class Acubiz_model:
    def __init__(self, uuid_userref, firstname, lastname, userid, email,
                 los_id, person_ref, manager_uuid_userref, longname, unic_userid, deleted,
                 opus_id, homeems, dim6, dim7):
        self.uuid_userref = uuid_userref
        self.name = firstname + ' ' + lastname
        self.userid = userid
        if userid is None:
            self.userid = unic_userid
            self.uuid_userref = unic_userid
        self.email = email
        if email is None and unic_userid is not None:
            self.email = unic_userid + '@skole.skanderborg.dk'
        self.los_id = los_id
        self.person_ref = person_ref
        self.manager_uuid_userref = manager_uuid_userref
        self.longname = longname
        self.deleted = deleted in ['true', 'True', 1]
        self.opus_id = int(opus_id)
        self.homeems = homeems
        self.dim6 = dim6
        self.dim7 = dim7