import os
from os.path import join, dirname
from dotenv import load_dotenv
from service.sofd_setup.sbsys_extensions_service import Sbsys_extensions_service

# Vi har vores hemmelige værdier i en .env fil, hvis du skal bruge scriptet skal du have styr på disse.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# starter vores e-mail service - henter smtp informationer fra .env fil
constr_lora = os.environ.get('constr_lora')
sbsys_extensionfield9 = os.environ.get('sbsys_extensionfield9')
sbsys_extensionfield10 = os.environ.get('sbsys_extensionfield10')

sbsys_extensions_service = Sbsys_extensions_service(constr_lora, sbsys_extensionfield9, sbsys_extensionfield10)
sbsys_extensions_service.update_sbsys_extensions()