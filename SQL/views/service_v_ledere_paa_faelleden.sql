/****** Object:  View [service].[v_ledere_paa_faelleden]    Script Date: 26-05-2021 09:04:21 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [service].[v_ledere_paa_faelleden]
AS
SELECT        org.longname AS orgenhed, pos.title AS stilling, pos.uuid_userref AS user_fk, org.pnr
FROM            pyt.positions AS pos INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id
WHERE        (pos.is_manager = 1) AND (org.pnr IN
                             (SELECT        pnr
                               FROM            service.pnrs_paa_faelleden AS fal)) AND (pos.uuid_userref IS NOT NULL)
GO