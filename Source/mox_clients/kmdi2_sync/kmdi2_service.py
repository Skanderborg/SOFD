from datetime import datetime
from mox_clients.kmdi2_sync.kmdi2_repo import Kmdl2_repo
from dal.orgunit_repo import Orgunit_repo
from mox_clients.kmdi2_sync.institution_model import Institution_model
from mox_clients.kmdi2_sync.kmdi2_employee_api import Kmdi2_employee_api
from mox_clients.kmdi2_sync.json_models import Employee_json_model

class Kmdi2_service:
    def __init__(self, constr):
        self.constr = constr
        self.kmdi2_repo = Kmdl2_repo(constr)
        self.kmdi2_employee_api = Kmdi2_employee_api(constr)

    def sync_employees_with_kmdi2(self, apikey, add_employee_url, get_employements_url, delete_employements_url):
        #institutions = self.get_kmdi2_institution_and_employee_tree()

        # henter org træet fra kmdi2 - dict af institions med kmdi2_inst_id som key, har dict med employees med ssn som key
        sofd_institutions = self.get_relevant_sofd_institutions_with_employees()
        kmdi2_institutions = self.kmdi2_employee_api.get_kmd_employements(get_employements_url, apikey)
        

        # tilføj nye ansatte til institutions
        print(len(sofd_institutions))
        institutions_with_new_employees = self.get_new_employees(sofd_institutions, kmdi2_institutions)
        if len(institutions_with_new_employees) > 0:
            for inst in institutions_with_new_employees:
                endpoint_url = add_employee_url + str(inst.kmdi2_inst_number)
                #print('Tilføjer nye ansaemployeestte til: ', endpoint_url)
                for emp in inst.employees:
                    res = self.kmdi2_employee_api.add_new_employee(endpoint_url, apikey, emp)
                    if res != 200:
                        raise NameError('API create problem for :', emp.get_str(), res.text)
                    #else:
                    #    print(emp.get_str())

        # fjern ansatte som har forladt skuden
        #print(len(sofd_institutions))
        deleted_employmentids = self.get_deleted_employee_kmdi2_ids(sofd_institutions, kmdi2_institutions)
        #print(len(deleted_employmentids))
        
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
                #henter de ansatte i forældre organsiationen, som skal med i underorganisationerne
                emps = self.kmdi2_repo.get_employees_in_orgunit(db_inst['parent_orgunit_los_id'])
                #henter child units, hvis de skal hentes
                #if db_inst['sync_children'] in ['true', 'True', 1]:
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #else:
                    #print('dagtilbud', los_id)
                #    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(los_id)
                for e in emps:
                    kmdi2role = self.get_kmdi2_role(e['title'])
                    if kmdi2role is not None:
                        tmp_inst.add_employee(self.create_employee(e, kmdi2role))
            else:
                #ikke dagtilbud
                emps = []
                #if db_inst['sync_children'] in ['true', 'True', 1]:
                    #henter child units, hvis de skal hentes
                inst_and_children = self.kmdi2_repo.get_orgunit_and_children(los_id)
                for tmp_los_id in inst_and_children:
                    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(tmp_los_id)
                #else:
                #    print('hej', los_id)
                #    emps = emps + self.kmdi2_repo.get_employees_in_orgunit(los_id)
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
            #når der kobles en ny institution på er den ikke nødvendigvis med fordi der ikke er medarbejdere i kmdi2 og derfor vil der ikke være en nøgle
            kmd_inst_emps = []
            if sofd_inst.kmdi2_inst_number in kmdi2_institutions:
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
            #print('inst:', sofd_inst.kmdi2_inst_number)
            #når der kobles en ny institution på er den ikke nødvendigvis med fordi der ikke er medarbejdere i kmdi2 og derfor vil der ikke være en nøgle
            tmp_inst_employees = []
            if sofd_inst.kmdi2_inst_number in kmdi2_institutions:
                tmp_inst_employees = kmdi2_institutions[sofd_inst.kmdi2_inst_number].get_employees()

            tmp_sofd_ssns = []
            for sofd_emp in sofd_inst.employees:
                tmp_sofd_ssns.append(sofd_emp.ssn)
            for kmd_emp_ssn in tmp_inst_employees:
                if kmd_emp_ssn not in tmp_sofd_ssns:
                    #print('slet', kmd_emp_ssn)
                    kmd_emp = tmp_inst_employees[kmd_emp_ssn]
                    #OBS, hvis skolebestyrelser eller lignende er tilføjet til aula manuelt skal de ikke slettes, derfor sletter vi kun de brugere som er oprettet automatisk
                    if kmd_emp.manuallyAdded == False:
                        employementids_result.append(kmd_emp.employmentId)
        return employementids_result


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
                {'title': 'Leder'}
                

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