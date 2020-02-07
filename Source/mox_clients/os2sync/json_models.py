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


class Generic_address_json:
    def __init__(self, Value):
        self.Value = Value

    def reprJSON(self):
        return dict(Value=self.Value)
