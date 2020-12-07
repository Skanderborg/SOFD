from datetime import datetime
from mox_clients.kmd_institution_api.kmdi2_repo import Kmdl2_repo
from dal.orgunit_repo import Orgunit_repo
from mox_clients.kmd_institution_api.institution_model import Institution_model
from mox_clients.kmd_institution_api.kmdi2_employee_api import Kmdi2_employee_api

class Kmdi2_service:
    def __init__(self, constr):
        self.constr = constr
        self.kmdi2_repo = Kmdl2_repo(constr)
        self.kmdi2_employee_api = Kmdi2_employee_api(self.constr)

    def print_orgs(self):
        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        insts = self.kmdi2_repo.get_institutions_to_sync()
        for key in insts:
            if key != 836727:
                continue
            inst = insts[key]
            if (inst['parent_orgunit_los_id'] in dagtilbud):
                print('Dagtilbud', inst['los_id'])
            else:
                print(inst['los_id'])

    def sync_employees_with_kmdi2(self, apikey, add_employee_url, get_employements_url):
        #institutions = self.get_kmdi2_institution_and_employee_tree()
        institutions = self.add_new_employees_to_kmdi2(apikey, get_employements_url)
        for inst in institutions:
            endpoint_url = add_employee_url + str(inst.kmdi2_inst_number)
            print(endpoint_url)
            print(len(inst.employees))
            for emp in inst.employees:
                res = self.kmdi2_employee_api.post_json(endpoint_url, apikey, emp)
                if res != 200:
                    raise NameError('API problem for :', emp.decode())
                else:
                    print(emp.decode())
    
    def add_new_employees_to_kmdi2(self, apikey, get_employements_url):
        '''
        Metode som opbygger en liste af orgunits, der skal synkroniseres til KMDi2 snitfladen, og disses medarbejdere
        Selve listen over org enhederne som skal synkroniseres vedligeholdes af børn og unge

        Hvis orgenheden er et dagtilbud (vedligeholdes også af børn og unge) skal medarbejderne i den overordnede (dagtilbuyddet)
        også synkes med i hver enhed
        '''

        # henter org træet fra kmdi2 - dict af institions med kmdi2_inst_id som key, har dict med employees med ssn som key
        kmdi2_employees = self.kmdi2_employee_api.get_kmd_employements(get_employements_url, apikey)

        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        institutions_result = []
        for los_id in institutions_to_sync:
            db_inst = institutions_to_sync[los_id]
            tmp_inst = Institution_model(db_inst['longname'], db_inst['kmdi2_id'])
            tmp_kmdi2_emps = kmdi2_employees[tmp_inst.kmdi2_inst_number].get_employees()
            institutions_result.append(tmp_inst)
            if (db_inst['parent_orgunit_los_id'] in dagtilbud):
                #hener de ansatte i forældre organsiationen, som skal med i underorganisationerne
                emps = self.kmdi2_repo.get_employees_in_orgunit(db_inst['parent_orgunit_los_id'])
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #robot tmp
                #emps = emps + self.kmdi2_repo.tmp_get_robotos()
                for e in emps:
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        if e['cpr'] not in tmp_kmdi2_emps:
                            tmp_inst.add_employee(self.create_employee(e, kmdi2role))
            else:
                emps = []
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #robot tmp
                #emps = emps + self.kmdi2_repo.tmp_get_robotos()
                for e in emps:
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        if e['cpr'] not in tmp_kmdi2_emps:
                            tmp_inst.add_employee(self.create_employee(e, kmdi2role))
        return institutions_result


    def get_kmdi2_institution_and_employee_tree(self):
        '''
        Metode som opbygger en liste af orgunits, der skal synkroniseres til KMDi2 snitfladen, og disses medarbejdere
        Selve listen over org enhederne som skal synkroniseres vedligeholdes af børn og unge

        Hvis orgenheden er et dagtilbud (vedligeholdes også af børn og unge) skal medarbejderne i den overordnede (dagtilbuyddet)
        også synkes med i hver enhed
        '''
        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        institutions_result = []
        for los_id in institutions_to_sync:
            db_inst = institutions_to_sync[los_id]
            tmp_inst = Institution_model(db_inst['longname'], db_inst['kmdi2_id'])
            institutions_result.append(tmp_inst)
            if (db_inst['parent_orgunit_los_id'] in dagtilbud):
                emps = self.kmdi2_repo.get_employees_in_orgunit(db_inst['parent_orgunit_los_id'])
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                for e in emps:
                    #if e['cpr'] == '':
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        tmp_inst.add_employee(self.create_employee(e, kmdi2role))
            else:
                emps = []
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                for e in emps:
                    #if e['cpr'] == '':
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        tmp_inst.add_employee(self.create_employee(e, kmdi2role))
        return institutions_result

    def create_employee(self, emp_db_model, kmdi2role):
        ssn = str(emp_db_model['cpr'])
        aliasName = emp_db_model['firstname'] + ' ' + emp_db_model['lastname']
        email = emp_db_model['Email']
        endDate = ''
        if emp_db_model['leave_date'] is not None and len(str(emp_db_model['leave_date'])) > 1:
            endDate =  emp_db_model['leave_date'].strftime('%m-%d-%y')
        startDate = emp_db_model['start_date'].strftime('%m-%d-%y')
        transferToUserAdministration = True
        mobilePhone ='87947000'
        if emp_db_model['WorkMobile'] is not None and len(emp_db_model['WorkMobile']) > 1:
            mobilePhone = emp_db_model['WorkMobile']
        workPhone = '87947000'
        if emp_db_model['Phone'] is not None and len(emp_db_model['Phone']) > 1:
            workPhone = emp_db_model['Phone']
        role_title = kmdi2role
        emp_json = self.kmdi2_employee_api.get_employee_as_json(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone, role_title)
        return emp_json

    
    def get_kmdi2_role(self, stilling):
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

            Oversættelser til skb stillinger - OBS skal flyttes fra repo til ngoet andet senere:
            institutionManager:
                {'title': 'Dagtilbudsleder'}
                {'title': 'Daglig leder'}
                {'title': 'Daginstitutionsleder'}

            management:
                {'title': 'Administrativ leder'}

            pedagogue:
                {'title': 'Pædagog'}
                {'title': 'Pædagogmedhjælper'}
                {'title': 'Pædagogisk assistent'}
                {'title': 'Pædagogstuderende'}
                {'title': 'Pædagogmedhjælper-vikar'}
                {'title': 'Praktikant'}

            substitute:
                {'title': 'Tilkaldevikar-Pædagogisk assistent'}
                {'title': 'Tilkaldevikar-Pædagogmedhjælper'}
                {'title': 'Tilkaldevikar-Pædagog'}
                {'title': 'Tilkaldevikar-Pædagogiskassistent'}
                {'title': 'Stedfortræder'}

            consultant:
                {'title': 'Ekstern'}
                {'title': 'Psykomotorisk terapeut'}

            tAP:
                {'title': 'Administrativ medarbejder'}
                {'title': 'Kommunikationsmedarbejder'}
                {'title': 'Ernæringsassistent'}
                {'title': 'Kostfaglig eneansvarlig'}
                {'title': 'Køkkenmedhjælper'}
                {'title': 'Køkkenassistent'}
                {'title': 'Ernæringsassistentelev'}
                {'title': 'Tilkaldevikar-Køkkenassistent'}
                {'title': 'Tilkaldevikar-Ernæringsassistent'}
                {'title': 'PB-Ernæring'}
                {'title': 'Køkkenmedhjælp'}
                {'title': 'Husassistent'}
                {'title': 'Tilkaldevikar-Husassistent'}
                {'title': 'Køkkenleder'}
        '''
        positiontitle_map = self.kmdi2_repo.get_kmd_sofd_positiontitle_map()
        stilling_lower = stilling.lower()
        if stilling_lower in positiontitle_map:
            return positiontitle_map[stilling_lower]
        else:
            return None