# SQL dokumentation

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

### Positions

### Persons

### Users

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

### qOrgunits

### qUsers

### qUsers_AD

### Triggers

## Log

### changes
### qOrgunits
### qUsers
