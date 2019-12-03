import json


class Sts_collection_json:
    def __init__(self):
        self.orgUnits = []
        self.users = []

    def add_org(self, org):
        self.orgUnits.append(org)

    def add_user(self, usr):
        self.users.append(usr)

    def reprJSON(self):
        return dict(orgUnits=self.orgUnits, users=self.users)


class Orgunit_json:
    def __init__(self, uuid, name, parentOrgUnitUuid, manager):
        self.uuid = uuid
        self.name = name
        self.parentOrgUnitUuid = parentOrgUnitUuid
        self.manager = manager

    def reprJSON(self):
        return dict(uuid=self.uuid, name=self.name, parentOrgUnitUuid=self.parentOrgUnitUuid, manager=self.manager)


class Manager_json:
    def __init__(self, uuid, userId):
        self.uuid = uuid
        self.userId = userId

    def reprJSON(self):
        return dict(uuid=self.uuid, userId=self.userId)


class User_json:
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


class Position_json:
    def __init__(self, name, orgUnitUuid):
        self.name = name
        self.orgUnitUuid = orgUnitUuid

    def reprJSON(self):
        return dict(name=self.name, orgUnitUuid=self.orgUnitUuid)
