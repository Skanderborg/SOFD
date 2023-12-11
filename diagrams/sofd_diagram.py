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


with Diagram('sofd_flow', show=False, direction='TB'):

    with Cluster('SOFD Core'):
        with Cluster('Cloud'):
            opus_integration = CloudServices('opus-integration')
            ad_integration = CloudServices('ad-integration')
            aws_s3 = SimpleStorageServiceS3('AWS S3')
            sofd_core =  VMClassic('SOFD Core')

        with Cluster('On premise'):
            ad_dispatcher = CloudServices('ad-dispatcher')
            skole_ad_dispatcher = CloudServices('skole-ad-dispatcher')
            opus_uploader = CloudServices('opus-uploader')
            ad_writeback = CloudServices('ad-writeback')
            replication_agent = CloudServices('replication agent')

    with Cluster('Data kilder'):
        opus_data = Boards('KMD OPUS data')
        uni_data = ActiveDirectory('Skanderborg Skole AD')
        ad_data = ActiveDirectory('Skanderborg AD')

    azure_services = ContainerInstances('Skanderborg Azure Automation')
    adfs = ActiveDirectory('Skanderborg ADFS')

    with Cluster('Integrationer'):
        mox_safetynet = CloudServicesClassic('mox_safetynet')
        mox_acubiz = CloudServicesClassic('mox_acubiz')
        mox_kmdi2 = CloudServicesClassic('mox_kmdi2_sync')
        mox_intranote = CloudServicesClassic('mox_intranote')
        os2sync = CloudServicesClassic('OS2Sync')
        os2rollekatalogsync = CloudServicesClassic('RollekatalogSync')


    with Cluster('SOFD'):
        sofden = SQLDatabases('LORA_SOFD')
        sofden - Redshift('logs')
        with Cluster('MOX agenter'):
            mox_kalenda_greenbyte = CloudServicesClassic('mox_kalenda_greenbyte')
    sofden - VMScaleSet('SKB Systemer')
    sts_org = Artifacts('STS Organisation')
    sts_org - VMScaleSet('KOMBIT Systemer')
    intranettet = VMClassic('Intranettet')
    kmd_i2 = VMClassic('KMD i2')
    aula = VMClassic('AULA')
    kalenda = VMClassic('Kalenda')
    kalenda - VMClassic('OPUS løn og personale')
    safetynet = VMClassic('Safetynet')
    acubiz = VMClassic('Acubiz')
    acubiz - MobileEngagement('Acubiz mobil App')
    kombit_context_handler = APIConnections('KOMBIT Contexthandler')
    os2_rollekatalog = VMClassic('OS2 Rollekatalog')

    #kø og mox
    ad_data >> adfs >> kombit_context_handler
    sts_org >> kombit_context_handler
    sofd_core >> mox_acubiz >> acubiz
    sofd_core >> mox_safetynet >> safetynet
    sofd_core >> mox_intranote >> intranettet
    sofd_core >> mox_kmdi2 >> kmd_i2 >> aula
    sofden >> mox_kalenda_greenbyte >> kalenda
    os2sync >> sts_org
    os2_rollekatalog >> kombit_context_handler
    #setup
    sofden >> azure_services >> ad_data >> azure_services >> sofden
    opus_data >> opus_uploader >> aws_s3 >> opus_integration >> sofd_core
    uni_data >> skole_ad_dispatcher >> ad_integration >> sofd_core
    uni_data >> ad_dispatcher >> ad_integration >> sofd_core
    ad_data >> ad_dispatcher >> ad_integration >> sofd_core
    sofd_core >> os2rollekatalogsync >> os2_rollekatalog
    sofd_core >> os2sync
    sofd_core >> replication_agent >> sofden
    sofd_core >> ad_writeback >> ad_data