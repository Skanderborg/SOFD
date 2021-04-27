from diagrams import Cluster, Diagram
from diagrams.azure.compute import ContainerInstances, CloudServices, CloudServicesClassic
from diagrams.azure.devops import Artifacts, Boards
from diagrams.azure.database import SQLDatabases
from diagrams.aws.integration import SQS
from diagrams.aws.database import Redshift
from diagrams.azure.identity import ActiveDirectory

with Diagram('SOFD flow', show=False, direction='TB'):

    with Cluster('Data kilder'):
        opus_data = Boards('Opus data')
        uni_data = Artifacts('WS17')
        ad_data = ActiveDirectory('AD')

    azure_services = ContainerInstances('Azure_services')


    with Cluster('SOFD'):
        with Cluster('Services'):
            opus_til_sofd = CloudServices('opus_til_sofd')
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
            
    sts_org = Artifacts('STS Organisation')
    intranettet = Artifacts('Intranettet')
    os2_rollekatalog = Artifacts('OS2 Rollekatalog')
    kmd_i2 = Artifacts('KMD i2 azure API')
    aula = Artifacts('AULA')
    kalenda = Artifacts('Kalenda')
    kalenda - Artifacts('OPUS løn og personale')


    #kø og mox
    sofden >> mox_kalenda_greenbyte >> kalenda
    sofden >> mox_intranote >> intranettet
    sofden >> mox_kmdi2 >> kmd_i2 >> aula
    queue >> mox_os2_sync >> sts_org
    sofden >> mox_os2_rolle >> os2_rollekatalog
    #setup
    sofden >> sofd_setup >> queue << sofden
    uni_data >> sofd_setup >> sofden
    opus_data >> opus_til_sofd >> sofden >> azure_services >> ad_data >> azure_services >> sofden
            

    

    