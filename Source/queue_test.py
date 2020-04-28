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
constr_lora = os.environ.get('constr_lora')



# add changes to queues
orgunit_queue_service = Orgunit_queue_service(constr_lora)
orgunit_queue_service.update_orgunit_queue()
step = 'orgunit_queue_service.update_orgunit_queue() complete'

#user_queue_service = User_queue_service(constr_lora)
#user_queue_service.update_user_queue()
#step = 'user_queue_service.update_user_queue() complete'