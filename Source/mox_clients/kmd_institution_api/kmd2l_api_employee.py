from json_models import Employee_json
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

    def create_json(self, ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone):
        employee_json = Employee_json(ssn, aliasName, email, endDate, startDate, transferToUserAdministration, mobilePhone, workPhone)
        #test_emp = test_employee_json(test_ssn, "fake person med fake cpr", "email@email.email", "01-01-2002", "01-01-2001", True, "12345678", "12345678")
        employee_json.add_role("teacher")
        result = json.dumps(employee_json.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def post_json(self, url, apikey, json_str):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code