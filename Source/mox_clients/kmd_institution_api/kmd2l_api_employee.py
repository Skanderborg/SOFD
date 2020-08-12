from json_models import Employee_json
from dal.orgunit_repo import Orgunit_Repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
import json, requests

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

class Kmd2l_api_employee:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def handle_employee_registration(self):
        org_repo = Orgunit_Repo(self.constr_lora)
        pos_repo = Position_Repo(self.constr_lora)
        usr_repo = User_repo(self.constr_lora)

    def create_employee(self, ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone):
        employee_json_model = Employee_json(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone)
        # aliasname er til brug for navn og addresse beskyttelse
        #test_emp = test_employee_json(test_ssn, "fake person med fake cpr", "email@email.email", "01-01-2002", "01-01-2001", True, "12345678", "12345678")
        return employee_json_model
    
    def add_role(self, employee_json_model, role):
        #roles skal undersøges om det er noget specielt
        employee_json_model.add_role(role)

    def create_employee_json(self, employee_json_model)
        result = json.dumps(employee_json_model.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def post_json(self, url, apikey, json_str):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code


        # skal slettes når de skrider fra SOFD




        """
        1
        Dagtilbudsområdet - alt under men ikke med
        
        2
        undtagelse: private institutioner - kører på losid


        3
        Det ansatte i de overordende org units, der hedder moget med
        dagtilbud, skal i stedet tilknyttes i alle deres direkte børn
        hvor der er medarbejdere.

        losid på dagtiblud - skal i db liste

        4
        KMD institution snitflade med pnumer eller institutions id.

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