import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.update_users_position_relation.user_position_service import User_position_service
from service.email_service import Email_service

'''
python app that builds the relation between users from AD and positions from Opus.
Needs to run after opus_xml_to_sofd.py has been executed
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

try:
    x = 1
except:
    es.send_mail('jacob.aagaard.bennike@skanderborg.dk',
                 'Error: update_users_position_relation python app', step)