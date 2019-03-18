USE [LORA_SOFD]
GO

/****** Object:  Trigger [queue].[TRG_FOR_DEL]
Script Date: 18-03-2019 10:31:33
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE TRIGGER [queue].[TRG_FOR_DEL]
ON [LORA_SOFD].[queue].[qOrgunits]
FOR DELETE
AS
     INSERT INTO [LORA_SOFD].[log].[qOrgunits] ([uuid], [los_id], [change_type], [Niveau], [time_changed])
     SELECT [uuid], [los_id], [change_type], [Niveau], [time_changed]
     FROM DELETED
GO


