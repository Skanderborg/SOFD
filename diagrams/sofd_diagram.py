from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS, EKS, Lambda
from diagrams.aws.database import Redshift
from diagrams.aws.integration import SQS
from diagrams.aws.storage import S3

with Diagram('SOFD flow', show=False, direction='LR'):

    with Cluster('Data kilder'):
        opus_data = EKS('Opus data')
        uni_data = EKS('WS17')
        ad_data = EKS('AD')

    azure_services = EKS('Azure_services')


    with Cluster('SOFD'):
        with Cluster('Services'):
            opus_til_sofd = ECS('opus_til_sofd')
            sofd_setup = ECS('sofd_setup')
        sofden = S3('SQL')
        sofden - ECS('logs')
        queue = SQS("Ændrings kø")
        with Cluster('MOX agenter'):
            os2_sync = ECS("OS2 Sync")
            os2_rolle = ECS('Sofd til rolle')
            
    sts_org = S3('STS Organisation')
    os2_rollekatalog = S3('OS2 Rollekatalog')


    #kø og mox
    queue >> os2_sync >> sts_org
    sofden >> os2_rolle >> os2_rollekatalog
    #setup
    sofden >> sofd_setup >> queue << sofden
    uni_data >> sofd_setup >> sofden
    opus_data >> opus_til_sofd >> sofden >> azure_services >> ad_data >> azure_services >> sofden
            

    

    