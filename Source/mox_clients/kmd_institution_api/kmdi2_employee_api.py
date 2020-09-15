from mox_clients.kmd_institution_api.json_models import Employee_json_model
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
import json, requests

class kmd_inst:
    def __init__(self, institutionId):
        self.institutionId = institutionId
        self.employees = {}

    def add_employee(self, id, kmd_employee):
        self.employees[id] = kmd_employee

    def get_employees(self):
        return self.employees

class kmd_employee:
    def __init__(self, ssn, id):
        self.ssn = ssn
        self.id = id

class Kmd_institution_api_employee:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

class ComplexEncoder(json.JSONEncoder):
    '''
    JSON decoder, udvidelse til pythons json bibliotek, anvendes fordi nogle af vores objekter kan indeholde objekter, noget
    der som standard ikke kan håndteres i pythons standard bibliotek. Dette giver os samtidig bedre mulighed for at styrer
    navngivningen af Json attributerne.
    # pylint: disable=E0202 - er fordi Visual Studio Codes pylint giver falsepositive på "An attribute affected in %s line %s hide this method"
    '''
    def default(self, obj): # pylint: disable=E0202
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)

class Kmdi2_employee_api:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def handle_employee_registration(self):
        org_repo = Orgunit_Repo(self.constr_lora)
        pos_repo = Position_Repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)

    

    def create_employee(self, ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone, role_title):
        '''
          "teacher",
          "pedagogue",
          "substitute",
          "institutionManager",
          "management",
          "tAP",
          "consultant"
        '''
        #test_emp = Employee_json_model(ssn, "fake person med fake cpr", "email@email.email", "01-31-2021", "02-01-2018", True, "12345678", "12345678")
        emp = Employee_json_model(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone)
        # aliasname er til brug for navn og addresse beskyttelse
        emp.add_role(role_title)
        result_json = json.dumps(emp.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result_json

    def post_json(self, url, apikey, json_str):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.post(url=url, headers=headers, data=json_str)
        print('status code:', response.status_code)
        print('headers:', response.headers)
        print('text:', response.text)
        return response.status_code


        # skal slettes når de skrider fra SOFD


    def get_kmd_employements(self, url, apikey):
        result_dict = {}
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.get(url=url, headers=headers)
        print('status code:', response.status_code)
        print('headers:', response.headers)
        print('text:', response.text)

        jdata = json.loads(response.text)
        for emp in jdata:
            int_id = emp['institutionId']
            kmd_emp = kmd_employee(emp['ssn'], emp['employmentId'])
            if int_id in result_dict:
                inst = result_dict[int_id]
                inst.add_employee(emp['employmentId'], kmd_emp)
            else:
                inst = kmd_inst(int_id)
                inst.add_employee(emp['employmentId'], kmd_emp)
                result_dict[int_id] = inst
        return result_dict
        '''
        for key in result_dict:
            inst = result_dict[key]
            emps = inst.get_employees()
            print(inst.institutionId)
            for k in emps:
                emp = emps[k]
                print(emp.ssn)
        '''
        



        """
        1
        Dagtilbudsområdet - alt under men ikke med
        
        2
        undtagelse: private institutioner - kører på losid


        3
        De ansatte i de overordende org units, der hedder moget med
        dagtilbud, skal i stedet tilknyttes i alle deres direkte børn
        hvor der er medarbejdere.

        losid på dagtiblud - skal i db liste

        4
        KMD institution snitflade med pnumer eller institutions id. æ- vi bruge den vi altid har det er id

        5
        adgang til KMD Institution API
        træk institutioner


        6.
        send liste over stillinger til kristian

        7. dagplejen skal afvente informatzion før den sendes


        SELECT p.opus_id,
	per.Firstname,
	per.Lastname,
	o.longname,
	p.title,
	p.title_short,
	p.paygrade_title
    FROM [LORA_SOFD].[sbsys].[sbsysusers_orgs] as s
    join [LORA_SOFD].[pyt].[positions] as p
    on p.opus_id = s.opus_id
  join [LORA_SOFD].[dbo].[Persons] as per
     on p.person_ref = per.Cpr
  join [LORA_SOFD].[pyt].[Orgunits] as o
  on p.los_id = o.los_id
  where extensionAttribute12 = 'Dagtilbudsområdet'
  order by longname

        """