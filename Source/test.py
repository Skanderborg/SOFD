import json


class Stsjson:
    def __init__(self):
        self.orgUnits = []
        self.users = []

    def add_org(self, org):
        self.orgUnits.append(org)

    def add_user(self, usr):
        self.users.append(usr)

    def reprJSON(self):
        return dict(orgUnits=self.orgUnits, users=self.users)


class Orgunit:
    def __init__(self, uuid, name, parentOrgUnitUuid, manager):
        self.uuid = uuid
        self.name = name
        self.parentOrgUnitUuid = parentOrgUnitUuid
        self.manager = manager

    def reprJSON(self):
        return dict(uuid=self.uuid, name=self.name, parentOrgUnitUuid=self.parentOrgUnitUuid)


class Manager:
    def __init__(self, uuid, userId):
        self.uuid = uuid
        self.userId = userId

        def reprJSON(self):
            return dict(uuid=self.uuid, userId=self.userId)


class User:
    def __init__(self, extUuid, userId, name, email):
        self.extUuid = extUuid
        self.userId = userId
        self.name = name
        self.email = email
        self.positions = []

    def add_position(self, position):
        self.positions.append(position)

    def reprJSON(self):
        return dict(extUuid=self.extUuid, userId=self.userId, name=self.name, email=self.email, positions=self.positions)


class Position:
    def __init__(self, name, orgUnitUuid):
        self.name = name
        self.orgUnitUuid = orgUnitUuid

    def reprJSON(self):
        return dict(name=self.name, orgUnitUuid=self.orgUnitUuid)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


js = Stsjson()
m1 = Manager("8431307b-3f09-442f-9113-7f6102d7520f", "jva")
m2 = Manager("9f367087-4050-40d4-b82e-64344d94e3e1", "aaa")
o1 = Orgunit("1c2986e2-7fcc-4599-a659-fd90e1d6efdc",
             "Von And Enterprises", None, m1)
o2 = Orgunit("494fcd55-f274-4884-a4ef-722a2fc4e23c", "Aktier",
             "1c2986e2-7fcc-4599-a659-fd90e1d6efdc", None)
o3 = Orgunit("039c774b-a71a-4448-b428-f81ae11cbe08",
             "Pedelafdelingen", "1c2986e2-7fcc-4599-a659-fd90e1d6efdc", m2)
js.add_org(o1)
js.add_org(o2)
js.add_org(o3)

p1 = Position("Bossen", "1c2986e2-7fcc-4599-a659-fd90e1d6efdc")
p2 = Position("Super pedel", "039c774b-a71a-4448-b428-f81ae11cbe08")
p3 = Position("Pedel", "494fcd55-f274-4884-a4ef-722a2fc4e23c")


u1 = User("8431307b-3f09-442f-9113-7f6102d7520f",
          "jva", "Joakim Von And", "jva@andeby.dk")
u1.add_position(p1)
u2 = User("9f367087-4050-40d4-b82e-64344d94e3e1",
          "aaa", "Anders And", "aaa@andeby.dk")
u2.add_position(p2)
u2.add_position(p3)

js.add_user(u1)
js.add_user(u2)

print(json.dumps(js.reprJSON(), cls=ComplexEncoder))
