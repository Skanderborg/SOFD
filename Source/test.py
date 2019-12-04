import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.sofd_setup.orgunit_queue_service import Orgunit_queue_service
from mox_clients.os2sync.os2sync_sync_service import Os2sync_sync_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')
step = 'setup complete'

qs = Orgunit_queue_service(constr_lora)

qs.run_orgunit_queue_setup()

qs.execute_stsorg_sync()
#qs.clean_orgunit_queue()