USE [LORA_SOFD]
GO

/****** Object:  Table [queue].[users_queue]    Script Date: 16-01-2020 14:00:13 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [queue].[users_queue](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[uuid] [nvarchar](200) NOT NULL,
	[opus_id] [int] NOT NULL,
	[change_type] [nvarchar](50) NOT NULL,
	[sts_org] [bit] NOT NULL,
	[date_added] [date] NOT NULL,
 CONSTRAINT [PK_users_queue] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [queue].[users_queue] ADD  CONSTRAINT [DF_users_queue_sts_org]  DEFAULT ((0)) FOR [sts_org]
GO

ALTER TABLE [queue].[users_queue] ADD  CONSTRAINT [DF_users_queue_date_added]  DEFAULT (getdate()) FOR [date_added]
GO


