/****** Object:  View [dbo].[v_info_to_AD]    Script Date: 26-05-2021 08:57:16 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[v_info_to_AD]
AS
SELECT        pos.uuid_userref AS ad_objectguid, pos.title, pos.opus_id AS employeenumber, pos.los_id AS orgid, org.longname AS department, org.city, org.zipcode AS postalcode, org.street AS streetaddress, 
                         pos.manager_opus_id AS manager_employeenumber, org.area AS company, lois.navn_tekst AS office
FROM            pyt.positions AS pos INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id INNER JOIN
                         LOIS.dbo.CVR_PROD_ENH AS lois ON org.pnr = lois.pnr
GO