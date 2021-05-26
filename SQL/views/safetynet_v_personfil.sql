/****** Object:  View [safetynet].[v_personfil]    Script Date: 26-05-2021 09:03:15 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create view [safetynet].[v_personfil] as

SELECT        OpusMedarbejderID AS Medarbejdernr, CPRnr AS [CPR-nr], Fornavn, Efternavn, LOSOrganisationID AS Afdelingskode, ErLeder, ArbejdsstedNavn AS Vejnavn, ArbejdsstedGade AS Husnr, ArbejdsstedPostnr AS Postnummer, 
                         Mail AS [Primær email], ADBrugerNavn AS [AD-brugernavn], start_date AS Ansættelsesdato, Fratraad_dato AS Fratrædelsesdato, StillingBetegnelse AS Stilling,
                             (SELECT        niveau
                               FROM            pyt.orgunits AS o
                               WHERE        (los_id = m.LOSOrganisationID)) AS Ledelsesniveau, NearmesteLederID AS [Leders MedarbejderNr],
                             (SELECT        CASE WHEN EXISTS
                                                             (SELECT        *
                                                               FROM            [MDM_SOFD_DB].[OPUS].[Function] AS oo
                                                               WHERE        oo.MedarbejderID = m.[MedarbejderID] AND oo.artText = 'Arbejdsmiljørepræsentant (AMR)') THEN CAST(1 AS bit) ELSE CAST(0 AS bit) END AS Expr1) AS ErARM
FROM            dbo.v_sofd_medarbejderoverblik AS m
WHERE        (numerator > 8) OR
                         (numerator = 8) AND (Ans_forhold = 01 OR
                         Ans_forhold = 00)
GO