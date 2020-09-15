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
        '''
        Metode som opbygger en liste af orgunits, der skal synkroniseres til KMDi2 snitfladen, og disses medarbejdere
        Selve listen over org enhederne som skal synkroniseres vedligeholdes af børn og unge

        Hvis orgenheden er et dagtilbud (vedligeholdes også af børn og unge) skal medarbejderne i den overordnede (dagtilbuyddet)
        også synkes med i hver enhed
        '''
        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        for los_id in institutions_to_sync:
            inst = institutions_to_sync[los_id]
            if (inst['parent_orgunit_los_id'] in dagtilbud):
                print('Dagtilbud', inst['longname'])
                emps = self.kmdi2_repo.get_employees_in_orgunit(inst['parent_orgunit_los_id'])
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                for e in emps:
                    print(e)
            else:
                print(inst['longname'])
                emps = []
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                for e in emps:
                    print(e)
    
    def get_kmdi2_stillingsbegreb(self, stilling):
        '''
        Metode som forsøger at matche OPUS stillinger med kmdi2 stillinger:
        ENUM med muligheder fra KMD:
            "teacher",
            "pedagogue",
            "substitute",
            "institutionManager",
            "management",
            "tAP",
            "consultant"
        '''
        result = ''

        return result