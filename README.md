# SOFD
Skanderborgs Organisations og Forretnings Databrønd.

## documentation
Skanderborgs SOFD landskab består af 3 forskellige versioner

* MDM - tidligere version af on-premise SOFD, som holdes ved lige grundet 3. parts afhængigheder
* LORA SOFD - nuværende version af on-premise SOFD. Holdes ved lige grundet 3. parts afhængigheder
* SOFD Core - nuværende cloud version af SOFD.

SOFD Core er den nyeste og primære SOFD. Data fra andre datakilder indlæses i SOFD Core via diverse standard SOFD Core komponenter.
Data i LORA SOFD er mestendels slave af data i SOFD Core, og data i MDM er slave af data i LORA SOFD.

### Data flows:
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/diagrams/sofd_flow.png)

### sofd_setup.py

Script, som bearbejder vores forretningsdata. Her tilføjes KOMBIT vendte UUID'er til Orgunits, og AD brugere + Positions tilknyttes til hinanden. Hver Orgunit bliver tilknyttet en leders Position, og hver Position bliver tilknyttet sin nærmeste Leder. Er et Skanderborg script, som ikke umiddelbart kan anvendes af andre, da det antager, at man har et AD dump i tabellerne Users og org_uiid, som er magen til vores.



## SQL dokumentation

### CREATE TABLE examples_
[Link til LORA SOFD SQL dokumentation](https://github.com/Skanderborg/SOFD/tree/master/SQL)