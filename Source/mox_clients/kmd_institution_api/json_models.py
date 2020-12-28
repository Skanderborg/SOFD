import json

class Employee_json_model:
    def __init__(self, ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone):
        self.ssn = ssn
        self.aliasName = aliasName
        self.email = email
        self.endDate = endDate
        self.startDate = startDate
        self.transferToUserAdministration = transferToUserAdministration
        self.roles = []
        self.mobilePhone = mobilePhone
        self.workPhone = workPhone

    def add_role(self, role):
        self.roles.append(role)

    def get_str(self):
        return 'SSN: ' + self.ssn + ' startdate: ' + self.startDate + ' role: ' + self.roles[0]

    def reprJSON(self):
        return dict(ssn=self.ssn, aliasName=self.aliasName, email=self.email, endDate=self.endDate,
                    startDate=self.startDate, transferToUserAdministration=self.transferToUserAdministration,
                    workPhone = self.workPhone, roles=self.roles, mobilePhone=self.mobilePhone)