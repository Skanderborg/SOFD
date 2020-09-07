from mox_clients.kmd_institution_api.kmdi2_repo import Kmdl2_repo
from dal.orgunit_repo import Orgunit_repo

class Kmdi2_service:
    def __init__(self, constr):
        self.kmdi2_repo = Kmdl2_repo(constr)

    def print_orgs(self):
        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        insts = self.kmdi2_repo.get_institutions_to_sync()
        for key in insts:
            inst = insts[key]
            if (inst['parent_orgunit_los_id'] in dagtilbud):
                print('Dagtilbud', inst['los_id'])
            else:
                print(inst['los_id'])
    
    def emp_test(self):
        self.kmdi2_repo.employees_in_tree()