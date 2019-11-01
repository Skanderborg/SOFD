import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.email_service import Email_service
from service.manager_setup_service import Manager_setup_service

'''
python app that handles the manager reference setup after the opus_xml_to_sofd has run.
author - Jacob Ågård Bennike
Skanderborg Kommune 2019
'''
# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
step = 'starting'


# connection string til SOFD databasen
constr_lora = os.environ.get('constr_lora')
ms = Manager_setup_service(constr_lora)
ms.set_orgunit_manager()

try:
    x = 1
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: manager_setup.py python app', step)
