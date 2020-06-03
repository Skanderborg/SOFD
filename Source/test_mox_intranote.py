import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.intranote.intranote_csv_service import Intranote_csv_service
from service.email_service import Email_service

#setup env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
#laod db constr
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
constr_lora = os.environ.get('constr_lora')
error_email = os.environ.get('error_email')

# intranote
intranote_csv_directory = os.environ.get('intranote_cvs_directory')
intranote_csv_service = Intranote_csv_service(constr_lora)
intranote_csv_service.create_orgunit_csv(intranote_csv_directory)
intranote_csv_service.create_users_csv(intranote_csv_directory)
intranote_csv_service.create_unic_csv(intranote_csv_directory)
