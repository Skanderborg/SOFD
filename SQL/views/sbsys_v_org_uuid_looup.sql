/****** Object:  View [sbsys].[v_org_uuid_lookup]    Script Date: 26-05-2021 09:03:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
create view [sbsys].[v_org_uuid_lookup] as
SELECT  [Uuid]
      ,[Los_id]
      ,[Name]
  FROM [LORA_SOFD].[dbo].[Orgunits]
GO