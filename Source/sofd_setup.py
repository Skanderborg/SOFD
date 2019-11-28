import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.email_service import Email_service
from service.sofd_setup.manager_setup_service import Manager_setup_service
from service.sofd_setup.user_position_service import User_position_service
from service.sofd_setup.orgunit_uuid_service import Orgunit_uuid_service

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

# '''
try:
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')
    step = 'setup complete'
    orgunit_uuid_service = Orgunit_uuid_service(constr_lora)
    step = 'orgunit_uuid_service complete'
    orgunit_uuid_service.set_orgunit_uuid()
    step = 'orgunit_uuid_service.set_parent_uuids() complete'
    orgunit_uuid_service.set_parent_uuids()
    step = 'org_service.set_orgunit_uuid() complete'

    # user_position_service skal eksekveres før manager setup fordi managerset up henter uuider som reference til leder
    user_position_service = User_position_service(constr_lora)
    step = 'user_position_service'
    user_position_service.link_user_to_position()
    step = 'user_position_service.link_user_to_position() complete'

    ms = Manager_setup_service(constr_lora)
    step = 'Manager_setup_service complete'
    ms.set_orgunit_manager()
    step = 'ms.set_orgunit_manager() complete'
    ms.set_nearest_manager()
    step = 'ms.set_nearest_manager() complete'

    step = 'finished'
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: manager_setup.py python app', step)


'''
constr_lora = os.environ.get('constr_lora')
step = 'setup complete'
orgunit_uuid_service = Orgunit_uuid_service(constr_lora)
step = 'orgunit_uuid_service complete'
orgunit_uuid_service.set_orgunit_uuid()
step = 'orgunit_uuid_service.set_parent_uuids() complete'
orgunit_uuid_service.set_parent_uuids()
step = 'org_service.set_orgunit_uuid() complete'

# user_position_service skal eksekveres før manager setup fordi managerset up henter uuider som reference til leder
user_position_service = User_position_service(constr_lora)
step = 'user_position_service'
user_position_service.link_user_to_position()
step = 'user_position_service.link_user_to_position() complete'
ms = Manager_setup_service(constr_lora)
step = 'Manager_setup_service complete'
ms.set_orgunit_manager()
step = 'ms.set_orgunit_manager() complete'
ms.set_nearest_manager()
step = 'ms.set_nearest_manager() complete'
step = 'finished'

# '''
