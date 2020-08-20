/****** Script for SelectTopNRows command from SSMS  ******/


create procedure get_all_orgunits_below @Parent int
as

WITH cte AS (SELECT        los_id, longname, parent_orgunit_los_id
                             FROM            pyt.Orgunits AS t
                             WHERE        (los_id = @Parent)
                             UNION ALL
                             SELECT        t.los_id, t.longname, t.parent_orgunit_los_id
                             FROM            pyt.Orgunits AS t INNER JOIN
                                                      cte ON t.parent_orgunit_los_id = cte.los_id)
    SELECT        los_id, longname, parent_orgunit_los_id
     FROM            cte