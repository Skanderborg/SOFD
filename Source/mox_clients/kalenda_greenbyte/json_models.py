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
    def __init__(self, org_id, parent_id, name, pnr):
        self.Id = org_id
        self.Parent_id = parent_id
        self.Name = name
        self.Pnr = pnr

    def reprJSON(self):
        return dict(Id=self.Id, Parent_id=self.Parent_id, Name=self.Name, Pnr=self.Pnr)


class Employee_json:
    def __init__(self, Employee_nr, Orgunit_id, Firstname, Lastname, Email, Samaccount, UUID, Is_manager, kmd_suppid, cpr, payment_method, org_pnr):
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
        self.Payment_method = payment_method
        self.Org_pnr = org_pnr

    def reprJSON(self):
        return dict(Employee_nr=self.Employee_nr, Orgunit_id=self.Orgunit_id, Firstname=self.Firstname, Lastname=self.Lastname, 
                    Email=self.Email, Samaccount=self.Samaccount, UUID=self.UUID, Is_manager=self.Is_manager, 
                    OpusMedarbejderExtraCiffer=self.OpusMedarbejderExtraCiffer, CPRnr=self.CPRnr, 
                    Payment_method = self.Payment_method, org_pnr = self.Org_pnr)