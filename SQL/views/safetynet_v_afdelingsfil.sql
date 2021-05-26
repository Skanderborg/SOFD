/****** Object:  View [safetynet].[v_afdelingsfil]    Script Date: 26-05-2021 09:02:52 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create view [safetynet].[v_afdelingsfil] as

WITH orgs AS (SELECT        los_id, parent_orgunit_los_id, longName, niveau
                                FROM            pyt.orgunits
                                WHERE        (los_id IN (822041))
                                UNION ALL
                                SELECT        c.los_id, c.parent_orgunit_los_id, c.longName, c.niveau
                                FROM            pyt.orgunits AS c INNER JOIN
                                                         orgs AS p ON c.parent_orgunit_los_id = p.los_id)
    SELECT        OrgUnit_1.los_id AS Afdelingskode, OrgUnit_1.longName AS Afdelingsnavn, OrgUnit_1.parent_orgunit_los_id AS Overafdelingskode, OrgUnit_1.pNr AS [VirksomhedsP.NR],
                                  (SELECT        longName
                                    FROM            pyt.Orgunits AS skborg
                                    WHERE        (parent_orgunit_los_id = 0)) AS Virksomhedsnavn
     FROM            orgs AS orgs_1 INNER JOIN
                              pyt.orgunits AS OrgUnit_1 ON OrgUnit_1.los_id = orgs_1.los_id
     WHERE        (OrgUnit_1.longName NOT LIKE '%#%')
GO