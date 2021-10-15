import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.kmdi2_sync.kmdi2_employee_api import Kmdi2_employee_api
from mox_clients.kmdi2_sync.kmd_institution_api import Kmd_institution_api
from mox_clients.kmdi2_sync.kmdi2_service import Kmdi2_service


# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
kmdi2_test_key = os.environ.get('kmdi2_test_key')
kmdi2_employee_api_key = os.environ.get('kmdi2_employee_api_key')
kmdi2_api_key = os.environ.get('kmdi2_api_key')

test_ssn = os.environ.get('test_ssn')

#Tilføj employees - 02-12-2020 - virker
add_employee_url = os.environ.get('kmdi2_employee_api_endpoint') + 'employment/institution/'
delete_employee_url = os.environ.get('kmdi2_employee_api_delete_endpoint')
get_employements_url = os.environ.get('kmdi2_employee_api_endpoint') + "employments"
constr_lora = os.environ.get('constr_lora')
kmdi2_service = Kmdi2_service(constr_lora)
kmdi2_service.sync_employees_with_kmdi2(kmdi2_employee_api_key, add_employee_url, get_employements_url, delete_employee_url)



# get employments - 02-12-2020 - virker men kræver ændringer i kmdi2employeeapi
#kmdi2_employee_api = Kmdi2_employee_api("constr_lora")
#get_employements_url = os.environ.get('kmdi2_employee_api_endpoint') + "employments"
#kmdi2_employee_api.get_kmd_employements(get_employements_url, kmdi2_employee_api_key)


# get institutions - 21-12-2020 virker fint
#kmd_institution_api_endpoint = os.environ.get('kmdi2_api_endpoint')
#kmd_institution_api = Kmd_institution_api()
#kmd_institution_api_url = kmd_institution_api_endpoint + 'institutions/simple'
#kmd_institution_api.get_institutions(kmd_institution_api_url, kmdi2_api_key)







# get employments
#kmdi2_employee_api = Kmdi2_employee_api("constr_lora")
#get_employements_url = os.environ.get('kmdi2_employee_api_endpoint') + "employments"
#kmdi2_employee_api.get_kmd_employements(get_employements_url, kmdi2_employee_api_key)

#kmd2l_api_employee = Kmdi2_employee_api("constr_lora")
#add_employee_url = os.environ.get('kmdi2_employee_api_test_endpoint') + 'employment/institution/' + "12"
#ssn = os.environ.get('test_ssn')
#json_data = kmd2l_api_employee.create_employee(ssn, "test", "test@skanderborg.dk", "01-31-2021", "02-01-2018", True, "12345678", "12345678", "consultant")
#print(json_data)
#kmd2l_api_employee.post_json(add_employee_url, kmdi2_test_key, json_data)


# add employee by institution id
#kmd2l_api_employee = Kmdi2_employee_api("constr_lora")
#add_employee_url = os.environ.get('kmdi2_employee_api_endpoint') + 'employment/institution/' + "2766"
#ssn = os.environ.get('ssn')
#json_data = kmd2l_api_employee.create_employee(ssn, "abs", "test@skanderborg.dk", "", "12-01-2015", True, "123", "123", "tAP")
#json_data = kmd2l_api_employee.create_employee(ssn, "abs", "test@skanderborg.dk", "", "01-01-2012", True, "123", "123", "tAP") - opus 52251
#json_data = kmd2l_api_employee.create_employee(ssn, "abs", "test@skanderborg.dk", "", "09-01-2000", True, "123", "123", "management")

#print(json_data)
#kmd2l_api_employee.post_json(add_employee_url, kmdi2_employee_api_key, json_data)