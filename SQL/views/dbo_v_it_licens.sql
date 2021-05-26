/****** Object:  View [dbo].[v_it_licens]    Script Date: 26-05-2021 08:57:50 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

create view [dbo].[v_it_licens] as
WITH orgs AS (SELECT        los_id, parent_orgunit_los_id, longName, niveau, ean
                                FROM            pyt.orgunits
                                WHERE        (parent_orgunit_los_id IN (847702, 834110, 878771, 878778, 878773, 878777, 878774, 878776, 878772, 859560, 871775, 874806, 834108, 847703, 851299, 846682)) OR
                                                          (los_id IN (847702, 834110, 878771, 878778, 878773, 878777, 878774, 878776, 878772, 859560, 871775, 874806, 834108, 847703, 851299, 846682))
                                UNION ALL
                                SELECT        c.los_id, c.parent_orgunit_los_id, c.longName, c.niveau, c.ean
                                FROM            pyt.orgunits AS c INNER JOIN
                                                         orgs AS p ON c.parent_orgunit_los_id = p.los_id)
    SELECT DISTINCT 
                              mm.Fornavn, mm.Efternavn, mm.StillingBetegnelse, mm.ArbejdsstedNavn, mm.LOSOrganisationsenhed, mm.NearmesteLederADBrugerID, mm.[start_date], mm.Fratraad_dato, mm.OPUSMedarbejderExtraCiffer, 
                              mm.numerator, mm.Omraede, mm.OmraedeID, mm.ErLeder, orgs_1.ean
     FROM            orgs AS orgs_1 INNER JOIN
                              dbo.v_sofd_medarbejderoverblik AS mm ON mm.LOSOrganisationID = orgs_1.los_id
GO