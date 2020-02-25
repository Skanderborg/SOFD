class Acubiz_model:
    def __init__(self, uuid_userref, firstname, lastname, userid, email, costcenter,
                 los_id, person_ref, manager_uuid_userref, longname, unic_userid):
        self.uuid_userref = uuid_userref
        self.name = firstname + ' ' + lastname
        self.userid = userid
        if userid is None:
            self.userid = unic_userid
            self.uuid_userref = unic_userid
        self.email = email
        self.costcenter = costcenter
        self.los_id = los_id
        self.person_ref = person_ref
        self.manager_uuid_userref = manager_uuid_userref
        self.longname = longname