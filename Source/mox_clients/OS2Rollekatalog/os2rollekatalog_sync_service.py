import json
from mox_clients.OS2Rollekatalog.json_models import Stsjson, Orgunit, Manager, User, Position


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class Os2rollekatalog_sync_service:

    def magic(self):
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
