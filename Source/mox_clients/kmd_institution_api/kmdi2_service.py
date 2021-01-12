from datetime import datetime
from mox_clients.kmd_institution_api.kmdi2_repo import Kmdl2_repo
from dal.orgunit_repo import Orgunit_repo
from mox_clients.kmd_institution_api.institution_model import Institution_model
from mox_clients.kmd_institution_api.kmdi2_employee_api import Kmdi2_employee_api
from mox_clients.kmd_institution_api.json_models import Employee_json_model

class Kmdi2_service:
    def __init__(self, constr, rpa_ssn):
        self.constr = constr
        self.kmdi2_repo = Kmdl2_repo(constr, rpa_ssn)
        self.kmdi2_employee_api = Kmdi2_employee_api(self.constr)

    def sync_employees_with_kmdi2(self, apikey, add_employee_url, get_employements_url, delete_employements_url):
        #institutions = self.get_kmdi2_institution_and_employee_tree()

        # henter org træet fra kmdi2 - dict af institions med kmdi2_inst_id som key, har dict med employees med ssn som key
        sofd_institutions = self.get_relevant_sofd_institutions_with_employees()
        kmdi2_institutions = self.kmdi2_employee_api.get_kmd_employements(get_employements_url, apikey)
        

        # tilføj nye ansatte til institutions
        
        institutions_with_new_employees = self.get_new_employees(sofd_institutions, kmdi2_institutions)
        if len(institutions_with_new_employees) > 0:
            for inst in institutions_with_new_employees:
                endpoint_url = add_employee_url + str(inst.kmdi2_inst_number)
                print('Tilføjer nye ansaemployeestte til: ', endpoint_url)
                for emp in inst.employees:
                    res = self.kmdi2_employee_api.add_new_employee(endpoint_url, apikey, emp)
                    if res != 200:
                        raise NameError('API create problem for :', emp.get_str())
                    else:
                        print(emp.get_str())

        # fjern ansatte som har forladt skuden
        deleted_employmentids = self.get_deleted_employee_kmdi2_ids(sofd_institutions, kmdi2_institutions)
        for employee_kmdid in deleted_employmentids:
            res = self.kmdi2_employee_api.delete_employement(delete_employements_url, apikey, employee_kmdid)
            if res != 200:
                raise NameError('API delete problem for :', employee_kmdid)

        # opdater ansatte


    def get_relevant_sofd_institutions_with_employees(self):
        '''
        Metode som ??

        Hvis orgenheden er et dagtilbud (vedligeholdes også af børn og unge) skal medarbejderne i den overordnede (dagtilbuyddet)
        også synkes med i hver enhed
        '''

        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        institutions_result = []
        for los_id in institutions_to_sync:
            db_inst = institutions_to_sync[los_id]
            tmp_inst = Institution_model(db_inst['longname'], db_inst['kmdi2_id'])
            if (db_inst['parent_orgunit_los_id'] in dagtilbud):
                #hener de ansatte i forældre organsiationen, som skal med i underorganisationerne
                emps = self.kmdi2_repo.get_employees_in_orgunit(db_inst['parent_orgunit_los_id'])
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #robot tmp
                emps = emps + self.kmdi2_repo.tmp_get_robotos()
                for e in emps:
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        tmp_inst.add_employee(self.create_employee(e, kmdi2role))
            else:
                emps = []
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #robot tmp
                emps = emps + self.kmdi2_repo.tmp_get_robotos()
                for e in emps:
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        tmp_inst.add_employee(self.create_employee(e, kmdi2role))
            institutions_result.append(tmp_inst)
        return institutions_result

    def get_new_employees(self, sofd_institutions, kmdi2_institutions):
        '''
        sofd_emps er objekter af classen Employee_json_model der findes i json_models.py

        '''
        institutions_result = []
        for sofd_inst in sofd_institutions:
            res_inst = Institution_model(sofd_inst.longname, sofd_inst.kmdi2_inst_number)
            kmd_inst_emps = kmdi2_institutions[sofd_inst.kmdi2_inst_number].get_employees()
            for sofd_emp in sofd_inst.employees:
                if sofd_emp.ssn not in kmd_inst_emps:
                    res_inst.add_employee(sofd_emp)
            if res_inst.get_employee_count() > 0:
                institutions_result.append(res_inst)
        return institutions_result

    def get_deleted_employee_kmdi2_ids(self, sofd_institutions, kmdi2_institutions):
        '''
        sofd_emps er objekter af classen Employee_json_model der findes i json_models.py
        kmd_emp er objekter af klassen Kmd_employee som findes i
        '''
        employementids_result = []
        for sofd_inst in sofd_institutions:
            tmp_inst_employees = kmdi2_institutions[sofd_inst.kmdi2_inst_number].get_employees()
            tmp_sofd_ssns = []
            for sofd_emp in sofd_inst.employees:
                 tmp_sofd_ssns.append(sofd_emp.ssn)
            for kmd_emp_ssn in tmp_inst_employees:
                if kmd_emp_ssn not in tmp_sofd_ssns:
                    kmd_emp = tmp_inst_employees[kmd_emp_ssn]
                    employementids_result.append(kmd_emp.employmentId)
        return employementids_result


    
    def add_new_employees_to_kmdi2(self, get_employements_url, kmdi2_institutions):
        '''
        depricated 28-12-2020
        Metode som opbygger en liste af orgunits, der skal synkroniseres til KMDi2 snitfladen, og disses medarbejdere
        Selve listen over org enhederne som skal synkroniseres vedligeholdes af børn og unge

        Hvis orgenheden er et dagtilbud (vedligeholdes også af børn og unge) skal medarbejderne i den overordnede (dagtilbuyddet)
        også synkes med i hver enhed
        '''

        # henter org træet fra kmdi2 - dict af institions med kmdi2_inst_id som key, har dict med employees med ssn som key
        #kmdi2_employees = self.kmdi2_employee_api.get_kmd_employements(get_employements_url, apikey)

        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        institutions_result = []
        for los_id in institutions_to_sync:
            db_inst = institutions_to_sync[los_id]
            tmp_inst = Institution_model(db_inst['longname'], db_inst['kmdi2_id'])
            tmp_kmdi2_emps = kmdi2_institutions[tmp_inst.kmdi2_inst_number].get_employees()
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


    def get_removed_employees_to_kmdi2(self, get_employements_url, kmdi2_institutions):
        '''
        never used, i think
        '''
        dagtilbud = self.kmdi2_repo.get_dagtilbud()
        institutions_to_sync = self.kmdi2_repo.get_institutions_to_sync()
        institutions_result = []

        #måske vi lige skal bygge sofd inst først

        for kmdi2_inst_id in kmdi2_institutions:
            kmdi2_inst = kmdi2_institutions[kmdi2_inst_id]
            kmdi2_inst_emps = kmdi2_inst.get_employees()
            sofd_emps = []
            for los_id in institutions_to_sync:
                sofd_inst = institutions_to_sync[los_id]
                if sofd_inst['kmdi2_id'] == kmdi2_inst_id:
                    if (sofd_inst['parent_orgunit_los_id'] in dagtilbud):
                        #hener de ansatte i forældre organsiationen, som skal med i underorganisationerne
                        sofd_emps = self.kmdi2_repo.get_employees_in_orgunit(sofd_inst['parent_orgunit_los_id'])
                        inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                        for tmp_los_id in inst_and_children:
                            sofd_emps = sofd_emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                            #robot tmp
                            #emps = emps + self.kmdi2_repo.tmp_get_robotos()
                    else:
                        inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                        for tmp_los_id in inst_and_children:
                            sofd_emps = sofd_emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                            #robot tmp
                            #emps = emps + self.kmdi2_repo.tmp_get_robotos()
            for ie in kmdi2_inst_emps:
                print(ie)
            for e in sofd_emps:
                print(e)
            break
            # nu er det jo bare sådan at los_id ikke er = kmdi_id fordi nogle kmd institutioner svare til flere los



    def get_kmdi2_institution_and_employee_tree(self):
        '''
        depricated 28-12-2020
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
        '''
        funktion der bygger og returner et Employee_json_model objekt af en employee, som er klart til at blive json.strinigied
        når det engang skal sendes til KMDI2 snitfladen
        Employee_json_model findes i json_models.py
        '''
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
        result_emp = Employee_json_model(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone)
        result_emp.add_role(kmdi2role)
        return result_emp

    
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