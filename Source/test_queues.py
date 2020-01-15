import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.queues.orgunit_queue_service import Orgunit_queue_service
from service.queues.user_queue_service import User_queue_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')

# opretter queue services
os = Orgunit_queue_service(constr_lora)
us = User_queue_service(constr_lora)


# opretter orgunit køen
os.create_orgunit_queue()

