import json


class Orgunit_json:
    def __init__(self, Uuid, ShortKey, Name, ParentOrgUnitUuid, Timestamp, Phone, Email):
        self.Uuid = Uuid
        self.ShortKey = ShortKey
        self.Name = Name
        self.ParentOrgUnitUuid = ParentOrgUnitUuid
        self.Timestamp = Timestamp
        self.Phone = Phone
        self.Email = Email
        self.ItSystemUuids = []

    def add_ItSystemUuids(self, ItSystemUuid):
        self.ItSystemUuids.append(ItSystemUuid)

    def reprJSON(self):
        return dict(Uuid=self.Uuid, ShortKey=self.ShortKey, Name=self.Name, ParentOrgUnitUuid=self.ParentOrgUnitUuid, Timestamp=self.Timestamp, Phone=self.Phone, Email=self.Email, ItSystemUuids=self.ItSystemUuids)


class Generic_address_json:
    def __init__(self, Value):
        self.Value = Value

    def reprJSON(self):
        return dict(Value=self.Value)
