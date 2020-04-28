USE [LORA_SOFD]
GO

/****** Object:  Trigger [pyt].[tgr_for_delete_on_positions]    Script Date: 28-04-2020 13:15:54 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		Jacob Ågård Bennike
-- Create date: 2020
-- Description:	<Description,,>
-- =============================================
CREATE TRIGGER [pyt].[tgr_for_delete_on_positions]
   ON  [LORA_SOFD].[pyt].[positions]
   FOR DELETE
AS 
	INSERT INTO [LORA_SOFD].[log].[positions_history]
	([action]
      ,[opus_id]
      ,[uuid_userref]
      ,[los_id]
      ,[person_ref]
      ,[kmd_suppid]
      ,[title]
      ,[position_id]
      ,[title_short]
      ,[paygrade_title]
      ,[is_manager]
      ,[payment_method]
      ,[payment_method_text]
      ,[weekly_hours_numerator]
      ,[weekly_hours_denominator]
      ,[invoice_recipient]
      ,[pos_pnr]
      ,[dsuser]
      ,[start_date]
      ,[leave_date]
      ,[manager_opus_id]
      ,[manager_uuid_userref])
	  SELECT
	  'Deleted'
	  ,[opus_id]
      ,[uuid_userref]
      ,[los_id]
      ,[person_ref]
      ,[kmd_suppid]
      ,[title]
      ,[position_id]
      ,[title_short]
      ,[paygrade_title]
      ,[is_manager]
      ,[payment_method]
      ,[payment_method_text]
      ,[weekly_hours_numerator]
      ,[weekly_hours_denominator]
      ,[invoice_recipient]
      ,[pos_pnr]
      ,[dsuser]
      ,[start_date]
      ,[leave_date]
      ,[manager_opus_id]
      ,[manager_uuid_userref]
  FROM DELETED

GO


