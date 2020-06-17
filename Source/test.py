import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.sofd_setup.unic_to_position_service import Unic_to_position_service


# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')

unic_to_position_service = Unic_to_position_service(constr_lora)
unic_to_position_service.bind_unic_to_position()


'''import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.queues.orgunit_queue_service import Orgunit_queue_service
from mox_clients.os2sync.os2sync_sync_service import Os2sync_sync_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
#constr_lora = os.environ.get('constr_lora')
#os2sync_apikey = os.environ.get('os2sync_apikey')
#os2sync_orgunit_endpoint = os.environ.get('os2sync_orgunit_endpointurl')
#os2sync_user_endpoint = os.environ.get('os2sync_user_endpointurl')
#step = 'setup complete'

#ms = Os2sync_sync_service(constr_lora, os2sync_apikey, os2sync_orgunit_endpoint)

#qs = Orgunit_queue_service(constr_lora)

#qs.run_orgunit_queue_setup()

#ms.sync_orgunits()
#qs.clean_orgunit_queue()
'''