import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from service.email_service import Email_service
from service.feriesaldo_to_sofd.feriesaldo_service import Feriesaldo_service


'''
python app that builds the SOFD feriesaldo from kmd's KFS delivery
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


'''try:
    x = 1
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: opus_xml_to_sofd python app', step)
'''

# henter stien til den sti hvor vores kfs-lan udtræk for OPUS medarbejder data er placeret
kfs_filepath = os.environ.get('feriesaldo_path')
# connection string til SOFD databasen
constr_lora = os.environ.get('constr_lora')
# finder frem til den seneste fil fra OPUS
list_of_files = glob.glob(kfs_filepath)
latest_file = max(list_of_files, key=os.path.getctime)
step = 'setup complete'
feriesaldo_Service = Feriesaldo_service(latest_file, constr_lora)
feriesaldo_Service.insert_feriesaldos_in_sofd()
# '''
