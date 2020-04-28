-- ================================================
-- Template generated from Template Explorer using:
-- Create Trigger (New Menu).SQL
--
-- Use the Specify Values for Template Parameters 
-- command (Ctrl-Shift-M) to fill in the parameter 
-- values below.
--
-- See additional Create Trigger templates for more
-- examples of different Trigger statements.
--
-- This block of comments will not be included in
-- the definition of the function.
-- ================================================
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Jacob Årgård Bennike
-- Create date: 2020
-- Description:	backups org units when they are deleted
-- =============================================
CREATE TRIGGER [pyt].[tgr_for_delete_on_orgunits]
   ON  [LORA_SOFD].[pyt].[Orgunits]
   FOR DELETE
AS 
	INSERT INTO [LORA_SOFD].[log].[orgunits_history]
           ([action],
		   [los_id], 
		   [uuid], 
		   [last_changed], 
		   [longname], 
		   [startdate], 
		   [enddate], 
		   [parent_orgunit_los_id], 
		   [parent_orgunit_uuid], 
		   [shortname], 
		   [street], 
		   [zipcode],
           [city],
           [phonenumber],
           [cvr],
           [ean],
           [seNr],
           [pnr],
           [orgtype],
           [orgtypetxt],
           [costcenter],
           [manager_opus_id],
           [hierarchy],
           [niveau],
           [area])
	SELECT 
	  'Deleted',
	  [los_id],
      [uuid],
      [last_changed],
      [longname],
      [startdate],
      [enddate],
      [parent_orgunit_los_id],
      [parent_orgunit_uuid],
      [shortname],
      [street],
      [zipcode],
      [city],
      [phonenumber],
      [cvr],
      [ean],
      [seNr],
      [pnr],
      [orgtype],
      [orgtypetxt],
      [costcenter],
      [manager_opus_id],
      [hierarchy],
      [niveau],
      [area]
	  FROM DELETED
GO

