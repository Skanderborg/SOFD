from mox_clients.kmdi2_sync.json_models import Employee_json_model
from dal.orgunit_repo import Orgunit_repo
from dal.users_repo import User_repo
from dal.position_repo import Position_repo
import json, requests

class Kmd_inst:
    def __init__(self, institutionId):
        self.institutionId = institutionId
        self.employees = {}

    def add_employee(self, id, kmd_employee):
        self.employees[id] = kmd_employee

    def get_employees(self):
        return self.employees

class Kmd_employee:
    def __init__(self, ssn, institutionId, employmentId, aliasName, endDate, roles, startDate, manuallyAdded):
        self.ssn = ssn
        self.institutionId = institutionId
        self.employmentId = employmentId
        self.aliasName = aliasName
        self.endDate = endDate
        self.roles = roles
        self.startDate = startDate
        self.manuallyAdded = manuallyAdded in ['true', 'True', 1]
        '''
        "institutionProductionNumber": null,
        "institutionDtrId": null,
        "institutionId": 2960,
        "manuallyAdded": false,
        "lastUpdate": "2020-10-02T04:16:27.6714044",
        "updatedBy": "System",
        "aliasName": null,
        "email": null,
        "endDate": "9999-12-31T23:59:59.9999999",
        "mobilePhone": null,
        "roles": [
        "Pedagogue"
        ],
        "startDate": "2011-02-14T00:00:00",
        "transferToUserAdministration": true,
        "workPhone": null
        '''

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

    def get_employee_as_json(self, ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone, role_title):
        '''
        Depricated 28-12-2020
        '''
        #test_emp = Employee_json_model(ssn, "fake person med fake cpr", "email@email.email", "01-31-2021", "02-01-2018", True, "12345678", "12345678")
        emp = Employee_json_model(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone)
        # aliasname er til brug for navn og addresse beskyttelse
        emp.add_role(role_title)
        result_json = json.dumps(emp.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result_json

    def add_new_employee(self, url, apikey, emp):
        #return 200
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        json_str = json.dumps(emp.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        #print(json_str)
        response = requests.post(url=url, headers=headers, data=json_str)
        #print('status code:', response.status_code)
        #print('headers:', response.headers)
        #print('text:', response.text)
        return response.status_code

    def delete_employement(self, url, apikey, employment_kmdid):
        #return 200
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        url = url + str(employment_kmdid)
        response = requests.delete(url=url, headers=headers)
        #print('status code:', response.status_code)
        #print('headers:', response.headers)
        #print('text:', response.text)
        return response.status_code

    def get_kmd_employements(self, url, apikey):
        result_dict = {}
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.get(url=url, headers=headers)
        #print('status code:', response.status_code)
        #print('headers:', response.headers)
        #print('text:', response.text)

        jdata = json.loads(response.text)
        for emp in jdata:
            int_id = emp['institutionId']
            # kig på ems
            #'''
            if int_id == 2752 or int_id == '2752':
                print(emp['ssn'], emp['institutionId'], emp['employmentId'], emp['aliasName'], emp['endDate'],
                        emp['roles'], emp['startDate'], emp['manuallyAdded'])

            #'''
            kmd_emp = Kmd_employee(emp['ssn'], emp['institutionId'], emp['employmentId'], emp['aliasName'], emp['endDate'],
                        emp['roles'], emp['startDate'], emp['manuallyAdded'])
            if int_id in result_dict:
                inst = result_dict[int_id]
                inst.add_employee(emp['ssn'], kmd_emp)
            else:
                inst = Kmd_inst(int_id)
                inst.add_employee(emp['ssn'], kmd_emp)
                result_dict[int_id] = inst
        return result_dict