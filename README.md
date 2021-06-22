# SOFD
Skanderborgs Organisations og Forretnings Databrønd.

## documentation
Vores SOFD består af en række Python scripts, der har forskelligt ansvar.

### opus_xml_to_sofd.py
Script, som omdanner KFS XML fil fra KMD til data i tabellerne Orgunits, Persons og Positions. Kan i princippet anvendes af alle kommuner, som får et XML udtræk fra OPUS.

### feriesaldo.py
Script, som omdanner KFS fil fra KMD til data i tabellen feriesaldo. Kan i princippet anvendes af alle kommuner, som får ferie udtræk fra OPUS LØN og Personale.

### sofd_setup.py
Script, som bearbejder vores forretningsdata. Her tilføjes KOMBIT vendte UUID'er til Orgunits, og AD brugere + Positions tilknyttes til hinanden. Hver Orgunit bliver tilknyttet en leders Position, og hver Position bliver tilknyttet sin nærmeste Leder. Er et Skanderborg script, som ikke umiddelbart kan anvendes af andre, da det antager, at man har et AD dump i tabellerne Users og org_uiid, som er magen til vores.

### Data flows:
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/diagrams/sofd_flow.png)

## SQL dokumentation
### CREATE TABLE examples_
[Link til LORA SOFD SQL dokumentation](https://github.com/Skanderborg/SOFD/tree/master/SQL)