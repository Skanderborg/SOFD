USE [LORA_SOFD]
GO

/****** Object:  StoredProcedure [kmdl2].[get_orgunit_employes]    Script Date: 15-09-2020 11:10:00 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


create procedure [kmdl2].[get_orgunit_employes] @los_id int
as
SELECT [opus_id]
      ,[los_id]
      ,[title]
      ,[title_short]
      ,[paygrade_title]
      ,[is_manager]
      ,[cpr]
      ,[firstname]
      ,[lastname]
      ,[display_firstname]
      ,[display_lastname]
  FROM [LORA_SOFD].[pyt].[positions] as pos
  join [LORA_SOFD].[pyt].[persons] as per
  on pos.person_ref = per.cpr
  where pos.deleted = 0 and los_id = @los_id


GO