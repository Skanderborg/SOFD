import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.email_service import Email_service
from service.sofd_setup.manager_setup_service import Manager_setup_service
from service.sofd_setup.user_position_service import User_position_service
from service.sofd_setup.orgunit_parent_uuid_service import Orgunit_parent_uuid_service

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

'''
try:
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')

    # skal kører før manager setup fordi managerset up henter uuider som reference til leder
    step = 'user position service'
    user_position_service = User_position_service(constr_lora)
    step = 'user_position_service.link_user_to_position()'
    user_position_service.link_user_to_position()

    step = "manger service"
    ms = Manager_setup_service(constr_lora)
    step = "ms.set_orgunit_manager()"
    ms.set_orgunit_manager()
    step = 'ms.set_nearest_manager()'
    ms.set_nearest_manager()

    step = 'finished'
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: manager_setup.py python app', step)


'''
constr_lora = os.environ.get('constr_lora')
user_position_service = User_position_service(constr_lora)
user_position_service.link_user_to_position()
ms = Manager_setup_service(constr_lora)
ms.set_orgunit_manager()
ms.set_nearest_manager()


orgunit_parent_uuid_service = Orgunit_parent_uuid_service(constr_lora)
orgunit_parent_uuid_service.set_parent_uuids()

# '''
