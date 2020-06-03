import json
import requests
from mox_clients.kmd_institution_api.test_api.json_models import employee_json

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


class Kmd_institution_api_employee:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def get_json(self, test_ssn):
        test_emp = employee_json(test_ssn, "fake person med fake cpr", "email@email.email", "01-01-2002", "01-01-2001", True, "12345678", "12345678")
        test_emp.add_role("teacher")
        result = json.dumps(test_emp.reprJSON(), cls=ComplexEncoder, ensure_ascii=False).encode('utf8')
        return result

    def post_json(self, url, apikey, json_str):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        req = requests.post(url=url, headers=headers, data=json_str)
        print(req.text)
        print(req.status_code)
        return req.status_code