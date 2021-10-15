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
from diagrams.aws.storage import SimpleStorageServiceS3

from diagrams.azure.compute import VMScaleSet, VMClassic


with Diagram('SOFD Core fase 1', show=False, direction='TB'):

    with Cluster('SOFD Core'):
        with Cluster('Cloud'):
            opus_integration = CloudServices('opus-integration')
            ad_integration = CloudServices('ad-integration')
            stil_integration = CloudServices('stil-integration')        
            aws_s3 = SimpleStorageServiceS3('AWS S3')
            sofd_core =  VMClassic('SOFD Core')
        with Cluster('On premise'):
            ad_dispatcher = CloudServices('ad-dispatcher')
            opus_uploader = CloudServices('opus-uploader')
            ad_writeback = CloudServices('ad-writeback')
            replication_agent = CloudServices('replication agent')
            sofd_core_onprem = SQLDatabases('SOFD Core kopi')
            

    with Cluster('Data kilder'):
        opus_data = Boards('KMD OPUS data')
        uni_data = DataBoxEdgeDataBoxGateway('STIL unilogin WS17')
        ad_data = ActiveDirectory('Skanderborg AD')

    azure_services = ContainerInstances('Skanderborg Azure Automation')
    adfs = ActiveDirectory('Skanderborg ADFS')

    with Cluster('SOFD'):
        sofden = SQLDatabases('LORA_SOFD')
        sofden - Redshift('logs')
        queue = SQS("Ændrings kø")
        with Cluster('MOX agenter'):
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

    #kø og mox
    ad_data >> adfs >> kombit_context_handler
    sts_org >> kombit_context_handler
    sofden >> mox_acubiz >> acubiz
    sofden >> mox_safetynet >> safetynet
    sofden >> mox_kalenda_greenbyte >> kalenda
    sofden >> mox_intranote >> intranettet
    sofden >> mox_kmdi2 >> kmd_i2 >> aula
    os2sync >> sts_org
    os2_rollekatalog >> kombit_context_handler
    #setup
    sofden >> azure_services >> ad_data >> azure_services >> sofden    
    opus_data >> opus_uploader >> aws_s3 >> opus_integration >> sofd_core
    uni_data >> stil_integration >> sofd_core    
    ad_data >> ad_dispatcher >> ad_integration >> sofd_core
    sofd_core >> os2_rollekatalog
    sofd_core >> os2sync
    sofd_core >> replication_agent >> sofd_core_onprem >> replication_agent >> sofden
    sofd_core >> ad_writeback >> ad_data
    replication_agent >> queue >> mox_acubiz