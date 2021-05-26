/****** Object:  View [sbsys].[v_user_uuid_lookup]    Script Date: 26-05-2021 09:03:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
create view [sbsys].[v_user_uuid_lookup] as
SELECT [Uuid]
      ,[UserId]
      ,[Opus_id]
  FROM [LORA_SOFD].[dbo].[Users]
  where deleted_in_ad = 0
GO