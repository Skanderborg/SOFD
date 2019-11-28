import json
from mox_clients.OS2Rollekatalog.json_models import Sts_collection_json, Orgunit_json, Manager_json, User_json, Position_json
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class Os2rollekatalog_sync_service:
    def __init__(self, lora_constr):
        self.lora_constr = lora_constr

    def create_org_json(self):
        x = 1

    def post_json(self, json):
        x = 2

    def magic(self):
        js = Sts_collection_json()
        m1 = Manager_json("8431307b-3f09-442f-9113-7f6102d7520f", "jva")
        m2 = Manager_json("9f367087-4050-40d4-b82e-64344d94e3e1", "aaa")
        o1 = Orgunit_json("1c2986e2-7fcc-4599-a659-fd90e1d6efdc",
                          "Von And Enterprises", None, m1)
        o2 = Orgunit_json("494fcd55-f274-4884-a4ef-722a2fc4e23c", "Aktier",
                          "1c2986e2-7fcc-4599-a659-fd90e1d6efdc", None)
        o3 = Orgunit_json("039c774b-a71a-4448-b428-f81ae11cbe08",
                          "Pedelafdelingen", "1c2986e2-7fcc-4599-a659-fd90e1d6efdc", m2)
        js.add_org(o1)
        js.add_org(o2)
        js.add_org(o3)

        p1 = Position_json("Bossen", "1c2986e2-7fcc-4599-a659-fd90e1d6efdc")
        p2 = Position_json(
            "Super pedel", "039c774b-a71a-4448-b428-f81ae11cbe08")
        p3 = Position_json("Pedel", "494fcd55-f274-4884-a4ef-722a2fc4e23c")

        u1 = User_json("8431307b-3f09-442f-9113-7f6102d7520f",
                       "jva", "Joakim Von And", "jva@andeby.dk")
        u1.add_position(p1)
        u2 = User_json("9f367087-4050-40d4-b82e-64344d94e3e1",
                       "aaa", "Anders And", "aaa@andeby.dk")
        u2.add_position(p2)
        u2.add_position(p3)

        js.add_user(u1)
        js.add_user(u2)

        print(json.dumps(js.reprJSON(), cls=ComplexEncoder))
