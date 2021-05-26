/****** Object:  View [dbo].[v_ledere_af_ledere]    Script Date: 26-05-2021 08:58:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
create view [dbo].[v_ledere_af_ledere] as SELECT 
       pos.[opus_id]
	  ,per.firstname
	  ,per.lastname
      ,pos.[title]
	  ,usr.Email
  FROM [LORA_SOFD].[pyt].[positions] as pos
  join [LORA_SOFD].[pyt].[persons] as per
  on pos.[person_ref] = per.[cpr]
  join [LORA_SOFD].[dbo].[Users] as usr
  on pos.[uuid_userref] = usr.Uuid
  where pos.opus_id in (select [manager_opus_id] FROM [LORA_SOFD].[pyt].[positions]
  where is_manager = 1)
  
GO