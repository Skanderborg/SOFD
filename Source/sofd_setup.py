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
try:
    # tilføjer UUID'er til orgunits, tilføjer bagefter deres parent UUID
    orgunit_uuid_service = Orgunit_uuid_service(constr_lora)
    step = 'orgunit_uuid_service.set_parent_uuids() started'
    orgunit_uuid_service.set_orgunit_uuid()
    step = 'org_service.set_orgunit_uuid() started'
    orgunit_uuid_service.set_parent_uuids()

    # user_position_service skal eksekveres før manager setup fordi managerset up henter uuider som reference til leder
    step = 'user_position_service.link_user_to_position() started'
    user_position_service = User_position_service(constr_lora)
    user_position_service.link_user_to_position()

    # tilføjer manager til de orgenheder, der har en. Sætter nærmeste leder på positions.
    manager_setup_service = Manager_setup_service(constr_lora)
    step = 'manager_setup_service.remove_deleted_managers_from_orgunits() started'
    manager_setup_service.remove_deleted_managers_from_orgunits()
    step = 'manager_setup_service.set_orgunit_manager() started'
    manager_setup_service.set_orgunit_manager()
    step = 'manager_setup_service.set_nearest_manager() started'
    manager_setup_service.set_nearest_manager()

    # finder og indsætter ferie saldo
    step = 'feriesaldo_Service.insert_feriesaldos_in_sofd() started'
    # henter stien til den sti hvor vores kfs-lan udtræk for OPUS medarbejder data er placeret
    kfs_filepath = os.environ.get('feriesaldo_path')
    # finder frem til den seneste fil fra OPUS
    list_of_feriesaldo_files = glob.glob(kfs_filepath)
    latest_feriesaldo_file = max(list_of_feriesaldo_files, key=os.path.getctime)
    feriesaldo_Service = Feriesaldo_service(latest_feriesaldo_file, constr_lora)
    feriesaldo_Service.insert_feriesaldos_in_sofd()

    # UNIC setup - Unic_to_position_service
    step = 'unic_to_position_service.bind_unic_to_position() setup started'
    unic_to_position_service = Unic_to_position_service(constr_lora)
    unic_to_position_service.bind_unic_to_position()

    # QUEUE sync - Orgunit_queue_service + User_queue_service
    step = 'orgunit_queue_service.update_orgunit_queue() started'
    orgunit_queue_service = Orgunit_queue_service(constr_lora)
    orgunit_queue_service.update_orgunit_queue()

    step = 'user_queue_service.update_user_queue() started'
    user_queue_service = User_queue_service(constr_lora)
    user_queue_service.update_user_queue()

    step = 'user_queue_service.clean_user_queue() started'
    user_queue_service.clean_user_queue()

    # sbsys_setup - tager lidt tid
    step = 'sbsys - starting'
    sbsys_extensionfield9 = os.environ.get('sbsys_extensionfield9')
    sbsys_extensionfield10 = os.environ.get('sbsys_extensionfield10')
    sbsys_extensions_service = Sbsys_extensions_service(constr_lora, sbsys_extensionfield9, sbsys_extensionfield10)
    sbsys_extensions_service.update_sbsys_extensions()

    step = 'finished'
except Exception as e:
    es.send_mail(error_email,
                 'Error: sofd_setup.py python app', 'Step: ' + step + ' - Exception: ' + str(e))