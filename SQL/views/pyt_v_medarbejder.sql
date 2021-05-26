/****** Object:  View [pyt].[v_medarbejder]    Script Date: 26-05-2021 09:02:25 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
create view [pyt].[v_medarbejder] as select per.[cpr]
      ,per.[firstname]
      ,per.[lastname]
      ,per.[address]
      ,per.[zipcode]
      ,per.[city]
      ,per.[country]
      ,pos.[opus_id]
      ,pos.[uuid_userref]
      ,pos.[los_id]
      ,pos.[kmd_suppid]
      ,pos.[title]
      ,pos.[position_id]
      ,pos.[title_short]
      ,pos.[paygrade_title]
      ,pos.[is_manager]
      ,pos.[payment_method]
      ,pos.[payment_method_text]
      ,pos.[weekly_hours_numerator]
      ,pos.[weekly_hours_denominator]
      ,pos.[invoice_recipient]
      ,pos.[pos_pnr]
      ,pos.[dsuser]
      ,pos.[start_date]
      ,pos.[leave_date]
      ,pos.[manager_opus_id]
      ,pos.[manager_uuid_userref]
	  ,usr.[Uuid]
      ,usr.[UserId]
      ,usr.[Email]
      ,usr.[Phone]
      ,usr.[WorkMobile]
  FROM [LORA_SOFD].[pyt].[positions] as pos
  left join [LORA_SOFD].[pyt].[persons] as per
  on pos.person_ref = per.cpr
  left join [LORA_SOFD].[dbo].[users] as usr
  on pos.opus_id = usr.Opus_id
GO