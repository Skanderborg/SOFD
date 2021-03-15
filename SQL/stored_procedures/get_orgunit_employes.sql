USE [LORA_SOFD]
GO

/****** Object:  StoredProcedure [kmdl2].[get_orgunit_employes]    Script Date: 15-03-2021 11:43:42 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE procedure [kmdl2].[get_orgunit_employes] @los_id int
as
SELECT pos.[opus_id]
      ,pos.[los_id]
      ,pos.[title]
      ,per.[cpr]
      ,per.[firstname]
      ,per.[lastname]
      ,per.[display_firstname]
      ,per.[display_lastname]
	  ,pos.[start_date]
	  ,pos.[leave_date]
	  ,usr.[Email]
	  ,usr.[Phone]
	  ,usr.[WorkMobile]
  FROM [LORA_SOFD].[pyt].[positions] as pos
  join [LORA_SOFD].[pyt].[persons] as per
  on pos.person_ref = per.cpr
  left join [LORA_SOFD].[dbo].[users] as usr
  on usr.Opus_id = pos.opus_id
  where pos.deleted = 0 and los_id = @los_id and pos.[start_date] < (GetDate() + 1)


GO