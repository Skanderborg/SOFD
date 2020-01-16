import os
from os.path import join, dirname
from dotenv import load_dotenv
from mox_clients.intranote.intranote_csv_service import Intranote_csv_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')
intranote_csv_directory = 'c:/work/'

intranote_csv_service = Intranote_csv_service(constr_lora)
intranote_csv_service.create_orgunit_csv(intranote_csv_directory)
intranote_csv_service.create_users_csv(intranote_csv_directory)