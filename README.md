# SOFD
Skanderborgs Organisations og Forretnings Databrønd.

## Indledning
Skanderborgs SOFD landskab består af 3 forskellige versioner

* SOFD Core - nuværende cloud version af SOFD.
* LORA SOFD - nuværende version af on-premise SOFD. Holdes ved lige grundet 3. parts afhængigheder
* MDM - tidligere version af on-premise SOFD, som holdes ved lige grundet 3. parts afhængigheder

SOFD Core er den nyeste og primære SOFD. Data fra andre datakilder indlæses i SOFD Core via diverse standard SOFD Core komponenter.
Data i LORA SOFD er mestendels slave af data i SOFD Core, og data i MDM er slave af data i LORA SOFD.

## Data flows:
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/diagrams/sofd_flow.png)

## SOFD Core komponenter

### opus-uploader
Onpremise windows service, der uploader XML fil med organisationsenheder og medarbejdere til SOFD Cores driftsmiljø

### ad-dispatcher
Onpremise windows service der sender brugere fra Active Directory til SOFD Cores driftsmiljø

### ad-writeback
Onpremise windows service der ajourfører Active Directory konti med oplysninger fra SOFD Core

### replication agent
Onpremise windows service der holder LORA SOFD ved lige ud fra data i SOFD Core

### opus-integration
Cloud integration der importerer OPUS XML fil SOFD Core

### ad-integration
Cloud integration der håndterer oprettelse/ændringing/sletning af AD-konti i SOFD Core

### stil-integration
Cloud integration der henter medarbejdere fra STILs WS17 (lærere) og læser dem ind i SOFD Core som STIL konti.

## LORA SOFD komponenter

### sofd_setup.py
Script der afvikler LORA Specifikke tilpasninger af data, herunder vedligehold af unic- og sbsys-tabeller.