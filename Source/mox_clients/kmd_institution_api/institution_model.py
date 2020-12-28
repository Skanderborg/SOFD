class Institution_model:
    def __init__(self, longname, kmdi2_inst_number):
        self.longname = longname
        self.kmdi2_inst_number = kmdi2_inst_number
        self.employees = []

    def get_employee_count(self):
        return len(self.employees)

    def add_employee(self, emp):
        self.employees.append(emp)