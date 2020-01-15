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


try:
    # connection string til SOFD databasen
    constr_lora = os.environ.get('constr_lora')
    step = 'setup complete'

    # tilføjer UUID'er til orgunits, tilføjer bagefter deres parent UUID
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

    # tilføjer manager til de orgenheder, der har en. Sætter nærmeste leder på positions.
    ms = Manager_setup_service(constr_lora)
    step = 'Manager_setup_service complete'
    ms.set_orgunit_manager()
    step = 'ms.set_orgunit_manager() complete'
    ms.set_nearest_manager()
    step = 'ms.set_nearest_manager() complete'

    # finder og indsætter ferie saldo
    # henter stien til den sti hvor vores kfs-lan udtræk for OPUS medarbejder data er placeret
    kfs_filepath = os.environ.get('feriesaldo_path')
    # finder frem til den seneste fil fra OPUS
    list_of_feriesaldo_files = glob.glob(kfs_filepath)
    latest_feriesaldo_file = max(list_of_feriesaldo_files, key=os.path.getctime)
    feriesaldo_Service = Feriesaldo_service(latest_feriesaldo_file, constr_lora)
    feriesaldo_Service.insert_feriesaldos_in_sofd()
    step = 'feriesaldo_Service.insert_feriesaldos_in_sofd() complete'

    # unic setup

    # add changes to queues
    orgunit_queue_service = Orgunit_queue_service(constr_lora)
    orgunit_queue_service.create_orgunit_queue()

    step = 'finished'
except:
    es.send_mail(error_email,
                 'Error: manager_setup.py python app', step)