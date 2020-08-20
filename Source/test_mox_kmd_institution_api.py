import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kmd_institution_api.test_api.kmd_institution_api_employee import Kmd_institution_api_employee
from mox_clients.kmd_institution_api.test_api.kmd_institution_api import Kmd_institution_api


# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
kmd_institution_api_test_Ocp_Apim_Subscription_Key = os.environ.get('kmd_institution_api_test_Ocp_Apim_Subscription_Key')
kmd_institution_employee_api_test_endpoint = os.environ.get('kmd_institution_employee_api_test_endpoint')
kmd_institution_api_test_endpoint = os.environ.get('kmd_institution_api_test_endpoint')
test_ssn = os.environ.get('test_ssn')

# get institutions
#kmd_institution_api = Kmd_institution_api()
#kmd_institution_api_url = kmd_institution_api_test_endpoint + 'institutions/simple'
#kmd_institution_api.get_institutions(kmd_institution_api_url, kmd_institution_api_test_Ocp_Apim_Subscription_Key)


# get employments
kmd_institution_api_employee = Kmd_institution_api_employee("constr_lora")
get_employements_url = kmd_institution_employee_api_test_endpoint + "employments"
kmd_institution_api_employee.get_kmd_employements(get_employements_url, kmd_institution_api_test_Ocp_Apim_Subscription_Key)

# add employee by institution id
#kmd_institution_api_employee = Kmd_institution_api_employee("constr_lora")
#add_employee_url = kmd_institution_employee_api_test_endpoint + 'employment/institution/' + "9"
#json_data = kmd_institution_api_employee.create_json(test_ssn)
#kmd_institution_api_employee.post_json(add_employee_url, kmd_institution_api_test_Ocp_Apim_Subscription_Key, json_data)