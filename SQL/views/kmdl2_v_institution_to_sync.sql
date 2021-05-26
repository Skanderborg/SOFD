/****** Object:  View [kmdl2].[v_institution_to_sync]    Script Date: 26-05-2021 08:53:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [kmdl2].[v_institution_to_sync]
AS
SELECT        i.system_id, i.los_id, i.kmdl2_id, i.kmdl2_name, o.longname, o.parent_orgunit_los_id, i.sync_children
FROM            kmdl2.institution_ids AS i INNER JOIN
                         pyt.Orgunits AS o ON i.los_id = o.los_id
GO