USE [LORA_SOFD]
GO

/****** Object:  Trigger [queue].[TRG_FOR_DEL_u]
Script Date: 18-03-2019 10:32:38
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE TRIGGER [queue].[TRG_FOR_DEL_u]
ON [LORA_SOFD].[queue].[qUsers]
FOR DELETE
AS
     INSERT INTO [LORA_SOFD].[log].[qUsers] ([uuid], [Opus_id], [change_type], [Time_added])
     SELECT [uuid], [Opus_id], [change_type], [Time_added]
     FROM DELETED

GO


