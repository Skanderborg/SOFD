import os
from os.path import join, dirname
from dotenv import load_dotenv
import glob
from mox_clients.acubiz.acubiz_csv_service import Acubiz_csv_service
from service.email_service import Email_service

#setup env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
#laod db constr
es = Email_service(os.environ.get('smtp_username'), os.environ.get(
    'smtp_password'), os.environ.get('smtp_server'), os.environ.get('smtp_port'))
constr_lora = os.environ.get('constr_lora')
error_email = os.environ.get('error_email')

acubiz_csv_directory = os.environ.get('acubiz_cvs_directory_test')
acubiz_csv_service = Acubiz_csv_service(constr_lora)
acubiz_csv_service.create_users_csv(acubiz_csv_directory)