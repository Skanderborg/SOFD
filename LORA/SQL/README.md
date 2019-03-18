# SQL dokumentation

## Diagram
Oversigt over LORA_SOFD databasen:

![Alt text](https://raw.githubusercontent.com/Skanderborg/SOFD/master/LORA/SQL/Lora_db_diagram.PNG)

## Business logic
### Orgunits
Tabel til opbevaring af de forskellige organisationsenheder i Skanderborg Kommune.

**Indeholder:**
```
[System_id] [int] IDENTITY(1,1) NOT NULL,
[Uuid] [nvarchar](200) NOT NULL,
[Los_id] [int] NOT NULL,
[Name] [nvarchar](max) NOT NULL,
[PayoutUnitUuid] [nvarchar](200) NOT NULL,
[Created_date] [datetime] NOT NULL,
[Phone] [nvarchar](200) NOT NULL,
[Email] [nvarchar](200) NOT NULL,
[Parent_losid] [int] NOT NULL,
[Los_short_name] [nvarchar](50) NOT NULL,
[Adress_ref] [int] NOT NULL,
[Last_changed] [datetime] NOT NULL,
[Ean] [bigint] NULL,
[Pnr] [bigint] NULL,
[Cost_center] [bigint] NULL,
[Org_type] [nvarchar](50) NOT NULL,
[Org_niveau] [int] NOT NULL,

Eks:
1
XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
XXXXXX
Skanderborg Kommune
1900-01-01 00:00:00.000
XXXXXXXX
skanderborg.kommune@skanderborg.dk
0
SKANDERB K
7535
2019-02-13 12:49:39.257
XXXXXXXXXXXXX
0
XXXXXXXXX
Organisation
0
```

Kendte Org_type værdier (dannes i LOS/OPUS):
* Afdeling
* Aktivitetscenter
* Bibliotek
* Bofællesskab
* Børnehave
* Daginstitution
* Direktion
* Distrikt
* Døgninstitution
* Enhed
* Fagcenter
* Fritidsklub
* Gruppe
* Hal
* Institution
* Juniorklub
* Kantine
* Kommunalbestyrelsen samt politikere
* Køkken
* Musikskole
* Område
* Organisation
* Projekt
* Skole
* Skolefritidsordning
* Sportsanlæg
* SSP
* Stab
* Tandplejeklinik
* Team
* Ungdomsklub
* Ungdomsskole
* Ældrecenter

## Brugeropjekter
OIOStandarden har en kortlægning af brugere, personer og ansættelser, som ikke findes i virkeligheden. F.eks. eksisterer en stilling, der ikke i nuet er besat af en medarbejder, ikke i vores organisationsdata. 
Derfor har vi opbygget en model der "oversætter" vores organisations data til en semi OIO-standard. Også fordi vi benytter disse data uden for OIO sammenhænge. Derfor består en ansættelse hos os af tre ting:

* En ansættelse (position)
* En person (Person)
* En IT bruger (User)

En Person kan være tilknyttet til flere ansættelser. I OIO kan en ansættelse være tilknyttet til flere IT brugere, men det er ikke noget vi operer med, da vi lader ObjectGUID i AD genere ansættelsens UUID.
**Dette er noget vi på sigt vil ændre.**.

### Positions
**Indeholder:**
```
[System_id] [int] IDENTITY(1,1) NOT NULL,
[Opus_id] [int] NOT NULL,
[Name] [nvarchar](max) NOT NULL,
[Orgunit_losid_fk] [int] NOT NULL,
[Person_fk] [nvarchar](50) NOT NULL,
[Ans_dato] [datetime] NOT NULL,
[Fra_dato] [datetime] NULL,
[Is_Manager] [bit] NOT NULL,
[Timetal] [decimal](28, 10) NOT NULL,
[Pay_method] [int] NOT NULL,
[Pay_method_text] [nvarchar](max) NOT NULL,
[Last_changed] [datetime] NOT NULL,
[User_fk] [nvarchar](200) NULL,

Eks:
50241
XXXXX
IT-udvikler
XXXXXXXXXX (cpr uden bindestreg)
2014-10-01 00:00:00.000
NULL
0
37.0000000000
1
Månedsløn bagud
2019-02-15 09:22:01.887
XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

### Persons
**Indeholder:**
```
[System_id] [int] IDENTITY(1,1) NOT NULL,
[Opus_id] [int] NOT NULL,
[Name] [nvarchar](max) NOT NULL,
[Orgunit_losid_fk] [int] NOT NULL,
[Person_fk] [nvarchar](50) NOT NULL,
[Ans_dato] [datetime] NOT NULL,
[Fra_dato] [datetime] NULL,
[Is_Manager] [bit] NOT NULL,
[Timetal] [decimal](28, 10) NOT NULL,
[Pay_method] [int] NOT NULL,
[Pay_method_text] [nvarchar](max) NOT NULL,
[Last_changed] [datetime] NOT NULL,
[User_fk] [nvarchar](200) NULL,

Eks:
50954
Jacob Hansen
XXXXXXXXXX (cpr uden bindestreg)
Jacob
Hansen
10672
2019-02-15 09:22:01.820
```

### Users
**OBS: Users er en tabel, der er delt mellem IT og LORA**

Når en AD bruger forandre sig, nedlægges eller opdateres, kører vores AD-services et script, som opdaterer "Updated" eller "Deleted_in_ad" felterne i Users tabellen. Dette sker fordi LORA_SOFD henter data direkte fra AD.
De data der hentes er:
* UUID - stammer fra ObjectGUID (bliver ændret på sigt)
* Samaccountname (UserId)
* Email
* Phone
* WorkMobile

**Indeholder:**
```
[System_id]
,[Uuid]
,[UserId]
,[Email]
,[Phone]
,[Opus_id]
,[Updated]
,[WorkMobile]
,[Deleted_in_ad]

Eks:
47045
XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
penyme
Jacob.Hansen@skanderborg.dk
+458794XXXX
XXXXX
0
NULL
0
```

### Adresses
Tabel, som indeholder forskellige adresser (ikke OIO, men fysiske adresser. De er delt mellem Users og Orgunits, og er helt bassalt en tabel, der søger for, at vi ikke opbevarer adresser flere gange i SOFDen.
**Indeholder:**
```
[system_id] [int] IDENTITY(1,1) NOT NULL,
[gade] [nvarchar](max) NOT NULL,
[postnr] [int] NOT NULL,
[by] [nvarchar](max) NOT NULL,

Eks:
1
Skanderborg Fællleden 1
8660
Skanderborg
```

## Queue
Når der sker opdateringer i DSA_SOFD, som er kilde data til LORA_SOFD, føres disse til forskellige kø'er, der håndteres efterfølgende. I nuværende version er det udelukkende brugere med en IT bruger, der er relvante for 
køerne.

### qOrgunits
Benyttes til at håndter de forandringer der sker med organisationsenheder.

Fra LORA_SOFD kan der være 3 actions:
* Created
* Updated
* Deleted

Der svarer til de forskellige actions, der kan være med en organisationsenhed.

**Indeholder:**
```
[queue].[qOrgunits](
[system_id] [int] IDENTITY(1,1) NOT NULL,
[uuid] [nvarchar](100) NULL,
[los_id] [int] NOT NULL,
[change_type] [nvarchar](10) NOT NULL,
[Niveau] [int] NOT NULL,
[time_changed] [datetime] NOT NULL,
```

### qUsers
Benyttes til at håndter de forandringer der sker med medarbejdere, som har en IT bruger tilknyttet sig i LORA_SOFD.

Fra LORA_SOFD kan der være 3 actions:
* Created
* Updated
* Deleted

Der svarer til de forskellige actions, der kan være med en medarbejder.

**Indeholder:**
```
[queue].[qUsers](
[System_id] [int] IDENTITY(1,1) NOT NULL,
[Uuid] [nvarchar](200) NULL,
[Opus_id] [int] NOT NULL,
[Change_type] [nvarchar](10) NOT NULL,
[Time_added] [datetime] NOT NULL,
```

### qUsers_AD
Benyttes til at adviserer AD om forandringer i SOFD'en. F.eks. når en bruger forsvinder, så denne kan få lukket sin AD konto. Der kører nogle IT-service scripts, som behandler disse informationer. 
(Disse scripts er ikke tilgængelige).

**Indeholder:**
```
[queue].[qUsers_AD](
[System_id] [int] IDENTITY(1,1) NOT NULL,
[Uuid] [nvarchar](200) NULL,
[EmployeeNumber] [int] NOT NULL,
[Manager] [nvarchar](250) NOT NULL,
[Company] [nvarchar](250) NOT NULL,
[Department] [nvarchar](250) NOT NULL,
[Office] [nvarchar](250) NOT NULL,
[StreetAddress] [nvarchar](250) NOT NULL,
[PostalCode] [nvarchar](250) NOT NULL,
[City] [nvarchar](250) NOT NULL,
[Title] [nvarchar](250) NOT NULL,
[Change_type] [nvarchar](10) NOT NULL,
[Time_added] [datetime] NOT NULL,
```

### Triggers
Når et kø element er behandlet, bliver det slettet. Der er opsat triggers, der gemmer ikke personfølsomme oplysninger om de forandringer der sker i LORA_SOFD. Det er typisk medarbejdernumre eller UUID'er samt den handling,
 der er foretaget, som bliver gemt. Så kan vi hvis det bliver nødvendigt, så f.eks. medarbejder nummer op i vores lønssystem og finde.

## Log
### changes
### qOrgunits
### qUsers
