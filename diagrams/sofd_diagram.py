from diagrams import Cluster, Diagram
from diagrams.azure.compute import ContainerInstances, CloudServices, CloudServicesClassic
from diagrams.azure.devops import Artifacts, Boards
from diagrams.azure.database import SQLDatabases
from diagrams.aws.integration import SQS
from diagrams.aws.database import Redshift
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.mobile import MobileEngagement
from diagrams.azure.storage import DataBoxEdgeDataBoxGateway
from diagrams.azure.web import APIConnections

from diagrams.azure.compute import VMScaleSet, VMClassic


with Diagram('SOFD flow', show=False, direction='TB'):

    with Cluster('Data kilder'):
        opus_data = Boards('KMD OPUS data')
        uni_data = DataBoxEdgeDataBoxGateway('STIL unilogin WS17')
        ad_data = ActiveDirectory('Skanderborg AD')

    azure_services = ContainerInstances('Skanderborg Azure Automation')
    adfs = ActiveDirectory('Skanderborg ADFS')

    with Cluster('SOFD'):
        with Cluster('Services'):
            opus_til_sofd = CloudServices('opus__xml_til_sofd')
            sofd_setup = CloudServices('sofd_setup')
        sofden = SQLDatabases('LORA_SOFD')
        sofden - Redshift('logs')
        queue = SQS("Ændrings kø")
        with Cluster('MOX agenter'):
            mox_os2_sync = CloudServicesClassic("mox_os2sync")
            mox_os2_rolle = CloudServicesClassic('mox_os2rollekatalog_sync')
            mox_kmdi2 = CloudServicesClassic('mox_kmdi2_sync')
            mox_intranote = CloudServicesClassic('mox_intranote')
            mox_kalenda_greenbyte = CloudServicesClassic('mox_kalenda_greenbyte')
            mox_safetynet = CloudServicesClassic('Safetynet SSIS service')
            mox_acubiz = CloudServicesClassic('mox_acubiz')
    sofden - VMScaleSet('SKB Systemer')
    sts_org = Artifacts('STS Organisation')
    sts_org - VMScaleSet('KOMBIT Systemer')
    intranettet = VMClassic('Intranettet')
    os2_rollekatalog = VMClassic('OS2 Rollekatalog')
    kmd_i2 = DataBoxEdgeDataBoxGateway('KMD i2 azure API')
    aula = VMClassic('AULA')
    kalenda = VMClassic('Kalenda')
    kalenda - VMClassic('OPUS løn og personale')
    safetynet = VMClassic('Safetynet')
    acubiz = VMClassic('Acubiz')
    acubiz - MobileEngagement('Acubiz mobil App')
    kombit_context_handler = APIConnections('KOMBIT Contaxhandler')
    os2sync = DataBoxEdgeDataBoxGateway('OS2Sync')
    #sbsys = Artifacts('SBSYS')
    #sbsys - Artifacts('SBSIP')


    #kø og mox
    #sofden >> sbsys >> azure_services
    ad_data >> adfs >> kombit_context_handler
    sts_org >> kombit_context_handler
    sofden >> mox_acubiz >> acubiz
    sofden >> mox_safetynet >> safetynet
    sofden >> mox_kalenda_greenbyte >> kalenda
    sofden >> mox_intranote >> intranettet
    sofden >> mox_kmdi2 >> kmd_i2 >> aula
    queue >> mox_os2_sync >> os2sync >> sts_org
    sofden >> mox_os2_rolle >> os2_rollekatalog >> kombit_context_handler
    #setup
    sofden >> sofd_setup >> queue << sofden
    uni_data >> sofd_setup >> sofden
    opus_data >> opus_til_sofd >> sofden >> azure_services >> ad_data >> azure_services >> sofden
            

    

    