/****** Object:  View [json].[orgunits_full]    Script Date: 26-05-2021 09:00:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
create view [json].[orgunits_full] as
SELECT [System_id]
      ,[Uuid]
      ,[Los_id]
      ,[Name]
      ,[PayoutUnitUuid]
      ,[Created_date]
      ,[Phone]
      ,[Email]
      ,[Parent_losid]
      ,[Los_short_name]
      ,[Adress_ref]
      ,[Last_changed]
      ,[Ean]
      ,[Pnr]
      ,[Cost_center]
      ,[Org_type]
      ,[Org_niveau]
  FROM [LORA_SOFD].[dbo].[Orgunits]
GO