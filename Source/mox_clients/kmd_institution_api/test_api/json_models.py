import json

class employee_json:
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

    def reprJSON(self):
        return dict(ssn=self.ssn, aliasName=self.aliasName, email=self.email, endDate=self.endDate,
                    startDate=self.startDate, transferToUserAdministration=self.transferToUserAdministration,
                    roles=self.roles, mobilePhone=self.mobilePhone, workPhone = self.workPhone)