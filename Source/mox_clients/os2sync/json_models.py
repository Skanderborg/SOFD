import json


class Orgunit_json:
    def __init__(self, Uuid, ShortKey, Name, ParentOrgUnitUuid, PhoneNumber, Email, PayoutUnitUuid=None,
                    Location=None, LOSShortName=None, ContactOpenHours=None, PhoneOpenHours=None, PostReturn=None,
                    EmailRemarks=None, Contact=None, Ean=None, Post=None, Url=None, Landline=None):
        self.Uuid = Uuid
        self.ShortKey = ShortKey
        self.Name = Name
        self.ParentOrgUnitUuid = ParentOrgUnitUuid
        self.PayoutUnitUuid = PayoutUnitUuid
        self.PhoneNumber = PhoneNumber
        self.Email = Email
        self.Location = Location
        self.LOSShortName = LOSShortName
        self.ContactOpenHours = ContactOpenHours
        self.PhoneOpenHours = PhoneOpenHours
        self.PostReturn = PostReturn
        self.EmailRemarks = EmailRemarks
        self.Contact = Contact
        self.Ean = Ean
        self.Post = Post
        self.Url = Url
        self.Landline = Landline
        self.Tasks = []
        self.ContactForTasks = []

    def add_Task(self, task):
        self.Tasks.append(task)

    def add_ContractForTasks(self, contract):
        self.ContactForTasks.append(contract)

    def reprJSON(self):
        return dict(Uuid=self.Uuid,
                    ShortKey=self.ShortKey,
                    Name=self.Name,
                    ParentOrgUnitUuid=self.ParentOrgUnitUuid,
                    PayoutUnitUuid=self.PayoutUnitUuid,
                    PhoneNumber=self.PhoneNumber,
                    Email=self.Email,
                    Location=self.Location,
                    LOSShortName=self.LOSShortName,
                    ContactOpenHours=self.ContactOpenHours,
                    PhoneOpenHours=self.PhoneOpenHours,
                    PostReturn=self.PostReturn,
                    EmailRemarks=self.EmailRemarks,
                    Contact=self.Contact,
                    Ean=self.Ean,
                    Post=self.Post,
                    Url=self.Url,
                    Landline=self.Landline,
                    Tasks=self.Tasks,
                    ContactForTasks=self.ContactForTasks)


class User_json:
    def __init__(self, Uuid, UserId, Email, Location, Person, ShortKey=None, PhoneNumber=None):
        self.Uuid = Uuid
        self.ShortKey = ShortKey
        self.UserId = UserId
        self.PhoneNumber = PhoneNumber
        self.Email = Email
        self.Location = Location
        self.Positions = []
        self.Person = Person

    def add_position(self, position):
        self.Positions.append(position)

    def reprJSON(self):
        return dict(Uuid=self.Uuid,
                    ShortKey=self.ShortKey,
                    UserId=self.UserId,
                    PhoneNumber=self.PhoneNumber,
                    Email=self.Email,
                    Location=self.Location,
                    Positions=self.Positions,
                    Person=self.Person)

class Person_json:
    def __init__(self, Name, Cpr=None):
        self.Name = Name
        self.Cpr = Cpr

    def reprJSON(self):
        return dict(Name=self.Name, Cpr=self.Cpr)

class Position_json:
    def __init__(self, OrgUnitUuid, Name):
        self.OrgUnitUuid = OrgUnitUuid
        self.Name = Name

    def reprJSON(self):
        return dict(OrgUnitUuid=self.OrgUnitUuid, Name=self.Name)
