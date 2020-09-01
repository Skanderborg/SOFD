import json
import requests
from mox_clients.kmd_institution_api.test_api.test_json_models import test_employee_json

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


    def get_kmd_employements(self, url, apikey):
        result_dict = {}
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.get(url=url, headers=headers)
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
        #return result_dict
        
        for key in result_dict:
            inst = result_dict[key]
            emps = inst.get_employees()
            print(inst.institutionId)
            for k in emps:
                emp = emps[k]
                print(emp.ssn)
        

        
    def create_employee_json(self, test_ssn):
        '''
        Creates a JSON template to post
        '''
        #test_emp = test_employee_json(ssn, "aliasname", "email@email.email", "enddate: mm-dd-yyyy -optional", "start date mm-dd-yyyy", True, "mobile 12345678", "phone 12345678")
        test_emp = test_employee_json(test_ssn, "fake person med fake cpr", "email@email.email", "05-31-2002", "04-31-2002", True, "12345678", "12345678")
        test_emp.add_role("teacher")
        result = json.dumps(test_emp.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def post_employee_json(self, url, apikey, json_str):
        '''
        Creates a new employee in the KMD systems
        '''
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code