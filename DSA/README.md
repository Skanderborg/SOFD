# DSA_SOFD
DSA_SOFD er en SQL database, der generes gennem en række Microsoft SSIS, som henter data fra forskelligek kilder. De tre primære kilder er fra OPUS løn og personale (medarbejder + ferie udtræk) og frA UNIC ws04 webservicen.

OBS: WS04 servicen bliver udfaset i 2019 og bliver i den forbindelse erstattet af ws17.

## SSIS flow:

### DSA_Main.dtsx
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/DSA/documentation/dsa_main_package.JPG)

### DSA_ADMedarbejder.dtsx
Flow der henter AD informationer ind fra en CSV fil, dette er per 24-06-2019 udelukkende til den gamle MDM_SOFD, men det skal selvfølgelig fortsætte ind til den er afviklet.
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/DSA/documentation/DSA_ADMedarbejder_package.jpg)

### DSA_Ferietimer.dtsx
Flow der indlæser KFS udtræk (linje udtræk) med ferie timer, og indsætter disse i en SQL tabel.
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/DSA/documentation/dsa_ferietimer_package.jpg)

### DSA_OPUSMedarbejder.dtsx
Flow der indlæser KFS udtræk (XML udtræk) med organisation og medarbejder informationer, og indsætter disse i en række sql tabeller.
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/DSA/documentation/dsa_opusmedarbejder_package.jpg)

### DSA_UNICAnsat.dtsx
Læser CSV fil, fra WS04 webservice udtræk.
OBS: bliver udfaset i løbet af 2019
![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/DSA/documentation/dsa_unicansat_package.jpg)

