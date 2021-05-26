/****** Object:  View [acubiz].[acubiz_to_csv]    Script Date: 26-05-2021 08:56:14 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [acubiz].[acubiz_to_csv]
AS
SELECT        pos.uuid_userref, per.firstname, per.lastname, us.UserId, us.Email, org.costcenter, pos.los_id, pos.person_ref, pos.manager_uuid_userref, org.longname, unic.unic_userid, pos.deleted, pos.opus_id, ef.ems, ef.dim6, 
                         ef.dim7
FROM            pyt.positions AS pos INNER JOIN
                         pyt.persons AS per ON pos.person_ref = per.cpr LEFT OUTER JOIN
                         dbo.Users AS us ON pos.uuid_userref = us.Uuid INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id LEFT OUTER JOIN
                         unic.unic_usernames AS unic ON unic.opus_id = pos.opus_id LEFT OUTER JOIN
                         acubiz.extra_fields AS ef ON ef.los_id = org.los_id
GO