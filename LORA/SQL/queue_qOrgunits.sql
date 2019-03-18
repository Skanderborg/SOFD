USE [LORA_SOFD]
GO

/****** Object:  Table [queue].[qOrgunits]
Script Date: 18-03-2019 10:28:22
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [queue].[qOrgunits](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[uuid] [nvarchar](100) NULL,
	[los_id] [int] NOT NULL,
	[change_type] [nvarchar](10) NOT NULL,
	[Niveau] [int] NOT NULL,
	[time_changed] [datetime] NOT NULL,
 CONSTRAINT [PK_qOrgunits] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [queue].[qOrgunits] ADD  CONSTRAINT [DF_qOrgunits_time_changed]  DEFAULT (getdate()) FOR [time_changed]
GO


