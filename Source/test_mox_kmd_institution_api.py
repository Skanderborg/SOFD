import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kmd_institution_api.test_api.kmd_institution_api_employee import Kmd_institution_api_employee


# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
kmd_institution_api_test_Ocp_Apim_Subscription_Key = os.environ.get('kmd_institution_api_test_Ocp_Apim_Subscription_Key')
kmd_institution_api_test_endpoint = os.environ.get('kmd_institution_api_test_endpoint')
test_ssn = os.environ.get('test_ssn')

kmd_institution_api_employee = Kmd_institution_api_employee("constr_lora")
url = kmd_institution_api_test_endpoint + "9"
json_data = kmd_institution_api_employee.get_json(test_ssn)
kmd_institution_api_employee.post_json(url, kmd_institution_api_test_Ocp_Apim_Subscription_Key, json_data)