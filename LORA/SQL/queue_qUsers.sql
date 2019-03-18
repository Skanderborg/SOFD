USE [LORA_SOFD]
GO

/****** Object:  Table [queue].[qUsers]
Script Date: 18-03-2019 10:29:49
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [queue].[qUsers](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Uuid] [nvarchar](200) NULL,
	[Opus_id] [int] NOT NULL,
	[Change_type] [nvarchar](10) NOT NULL,
	[Time_added] [datetime] NOT NULL,
 CONSTRAINT [PK_qEmployees] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [queue].[qUsers] ADD  CONSTRAINT [DF_qEmployees_Time_added]  DEFAULT (getdate()) FOR [Time_added]
GO
