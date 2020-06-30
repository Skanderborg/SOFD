import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from service.email_service import Email_service
from service.sofd_setup.manager_setup_service import Manager_setup_service
from service.sofd_setup.user_position_service import User_position_service
from service.sofd_setup.orgunit_uuid_service import Orgunit_uuid_service
from service.sofd_setup.feriesaldo_service import Feriesaldo_service
from service.queues.orgunit_queue_service import Orgunit_queue_service
from service.queues.user_queue_service import User_queue_service
from service.sofd_setup.sbsys_extensions_service import Sbsys_extensions_service
from service.sofd_setup.unic_to_position_service import Unic_to_position_service

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
error_email = os.environ.get('error_email')
step = 'starting'

# connection string til SOFD databasen
constr_lora = os.environ.get('constr_lora')
step = 'setup complete'

# user_position_service skal eksekveres før manager setup fordi managerset up henter uuider som reference til leder
user_position_service = User_position_service(constr_lora)
step = 'user_position_service'
user_position_service.link_user_to_position()
step = 'user_position_service.link_user_to_position() complete'

