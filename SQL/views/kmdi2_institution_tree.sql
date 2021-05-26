/****** Object:  View [kmdl2].[institution_tree]    Script Date: 26-05-2021 09:01:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [kmdl2].[institution_tree]
AS
WITH cte AS (SELECT        los_id, longname, parent_orgunit_los_id
                             FROM            pyt.Orgunits AS t
                             WHERE        (los_id = 834109)
                             UNION ALL
                             SELECT        t.los_id, t.longname, t.parent_orgunit_los_id
                             FROM            pyt.Orgunits AS t INNER JOIN
                                                      cte AS cte_2 ON t.parent_orgunit_los_id = cte_2.los_id)
    SELECT        los_id, longname, parent_orgunit_los_id
     FROM            cte AS cte_1
     WHERE        (los_id NOT LIKE 834109)
GO