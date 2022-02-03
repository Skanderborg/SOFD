from diagrams import Cluster, Diagram, Edge
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


with Diagram('sofd_flow_simple', show=False, direction='TB'):

    sofd_core =  VMClassic('SOFD Core')
            

    with Cluster('Data kilder'):
        opus_data = Boards('KMD OPUS data')
        uni_data = DataBoxEdgeDataBoxGateway('STIL unilogin WS17')
        ad_data = ActiveDirectory('Skanderborg AD')

    azure_services = ContainerInstances('Skanderborg Azure Automation')
    adfs = ActiveDirectory('Skanderborg ADFS')

    lora = SQLDatabases('LORA_SOFD')

    sts_org = Artifacts('STS Organisation')
    os2rollekatalog = VMClassic('OS2rollekatalog')
    os2faktor = VMClassic('OS2faktor')
    kombit_context_handler = APIConnections('KOMBIT Contexthandler')
    os2sync = DataBoxEdgeDataBoxGateway('OS2sync')

    ad_data >> adfs >> kombit_context_handler
    sts_org >> kombit_context_handler
    os2sync >> sts_org
    os2rollekatalog >> kombit_context_handler


    lora >> azure_services >> ad_data >> azure_services >> lora
    opus_data >> sofd_core
    uni_data >> sofd_core    
    ad_data >> sofd_core
    sofd_core >> os2rollekatalog
    sofd_core >> os2sync
    sofd_core >> lora
    sofd_core >> ad_data
    sofd_core >>  Edge(color="darkorange", style="bold") >> os2faktor
    os2rollekatalog >> Edge(color="darkorange", style="bold") >> os2faktor
    os2faktor >> Edge(color="darkorange", style="bold") >> ad_data