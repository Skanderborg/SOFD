import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kmd_institution_api.kmdi2_employee_api import Kmdi2_employee_api
from mox_clients.kmd_institution_api.test_api.kmd_institution_api import Kmd_institution_api


# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
kmdi2_test_key = os.environ.get('kmdi2_test_key')
kmdi2_employee_api_key = os.environ.get('kmdi2_employee_api_key')
kmdi2_api_key = os.environ.get('kmdi2_api_key')

test_ssn = os.environ.get('test_ssn')

# get institutions
#kmd_institution_api_endpoint = os.environ.get('kmd_institution_api_prod_endpoint')
#kmd_institution_api = Kmd_institution_api()
#kmd_institution_api_url = kmd_institution_api_endpoint + 'institutions/simple'
#kmd_institution_api.get_institutions(kmd_institution_api_url, kmd_institution_api_prod_primarykey)


# get employments
#kmdi2_employee_api = Kmdi2_employee_api("constr_lora")
#get_employements_url = os.environ.get('kmdi2_employee_api_endpoint') + "employments"
#kmdi2_employee_api.get_kmd_employements(get_employements_url, kmdi2_employee_api_key)

# add employee by institution id
kmd2l_api_employee = Kmdi2_employee_api("constr_lora")
add_employee_url = os.environ.get('kmdi2_employee_api_endpoint') + 'employment/institution/' + "2788"
ssn = os.environ.get('ssn')

print(json_data)
kmd2l_api_employee.post_json(add_employee_url, kmdi2_employee_api_key, json_data)