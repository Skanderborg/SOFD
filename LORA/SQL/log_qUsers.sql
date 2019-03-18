USE [LORA_SOFD]
GO

/****** Object:  Table [log].[qUsers]
Script Date: 18-03-2019 10:27:32
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [log].[qUsers](
	[System_id] [bigint] IDENTITY(1,1) NOT NULL,
	[Uuid] [nvarchar](200) NULL,
	[Opus_id] [int] NOT NULL,
	[Change_type] [nvarchar](10) NOT NULL,
	[Time_added] [datetime] NOT NULL,
 CONSTRAINT [PK_log_qEmployees] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO