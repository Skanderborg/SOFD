import json


class Collection_json:
    def __init__(self):
        self.Orgunits = []
        self.Employees = []

    def add_org(self, org):
        self.Orgunits.append(org)

    def add_emp(self, usr):
        self.Employees.append(usr)

    def reprJSON(self):
        return dict(Orgunits=self.Orgunits, Employees=self.Employees)


class Orgunit_json:
    def __init__(self, Id, Parent_id, Name):
        self.Id = Id
        self.Parent_id = Parent_id
        self.Name = Name

    def reprJSON(self):
        return dict(Id=self.Id, Parent_id=self.Parent_id, Name=self.Name)


class Employee_json:
    def __init__(self, Employee_nr, Orgunit_id, Firstname, Lastname, Email, Samaccount, UUID, Is_manager, kmd_suppid, cpr):
        self.Employee_nr = Employee_nr
        self.Orgunit_id = Orgunit_id
        self.Firstname = Firstname
        self.Lastname = Lastname
        self.Email = Email
        self.Samaccount = Samaccount
        self.UUID = UUID
        self.Is_manager = Is_manager
        self.OpusMedarbejderExtraCiffer = kmd_suppid
        self.CPRnr = cpr

    def reprJSON(self):
        return dict(Employee_nr=self.Employee_nr, Orgunit_id=self.Orgunit_id, Firstname=self.Firstname, Lastname=self.Lastname, 
                    Email=self.Email, Samaccount=self.Samaccount, UUID=self.UUID, Is_manager=self.Is_manager, 
                    OpusMedarbejderExtraCiffer=self.OpusMedarbejderExtraCiffer, CPRnr=self.CPRnr)