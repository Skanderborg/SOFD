from diagrams import Cluster, Diagram
from diagrams.azure.compute import ContainerInstances, CloudServices, CloudServicesClassic
from diagrams.azure.devops import Artifacts, Boards
from diagrams.azure.database import SQLDatabases
from diagrams.aws.integration import SQS
from diagrams.aws.database import Redshift
from diagrams.azure.identity import ActiveDirectory

with Diagram('SOFD flow', show=False, direction='TB'):

    with Cluster('Data kilder'):
        opus_data = Boards('KMD OPUS data')
        uni_data = Artifacts('UNINET_WS17')
        ad_data = ActiveDirectory('Skanderborg AD')

    azure_services = ContainerInstances('Skanderborg Azure services')
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
            
    sts_org = Artifacts('STS Organisation')
    sts_org - Artifacts('KOMBIT Systemer')
    intranettet = Artifacts('Intranettet')
    os2_rollekatalog = Artifacts('OS2 Rollekatalog')
    kmd_i2 = Artifacts('KMD i2 azure API')
    aula = Artifacts('AULA')
    kalenda = Artifacts('Kalenda')
    kalenda - Artifacts('OPUS løn og personale')
    safetynet = Artifacts('Safetynet')
    acubiz = Artifacts('Acubiz')
    acubiz - Artifacts('Acubiz mobil App')
    kombit_context_handler = Artifacts('KOMBIT Contaxhandler')


    #kø og mox
    ad_data >> adfs >> kombit_context_handler
    sts_org >> kombit_context_handler
    sofden >> mox_acubiz >> acubiz
    sofden >> mox_safetynet >> safetynet
    sofden >> mox_kalenda_greenbyte >> kalenda
    sofden >> mox_intranote >> intranettet
    sofden >> mox_kmdi2 >> kmd_i2 >> aula
    queue >> mox_os2_sync >> sts_org
    sofden >> mox_os2_rolle >> os2_rollekatalog >> kombit_context_handler
    #setup
    sofden >> sofd_setup >> queue << sofden
    uni_data >> sofd_setup >> sofden
    opus_data >> opus_til_sofd >> sofden >> azure_services >> ad_data >> azure_services >> sofden
            

    

    