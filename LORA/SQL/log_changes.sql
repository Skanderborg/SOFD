USE [LORA_SOFD]
GO

/****** Object:  Table [log].[changes]
Script Date: 18-03-2019 10:25:14
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [log].[changes](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[change_text] [nvarchar](max) NOT NULL,
	[change_date] [datetime] NOT NULL,
	[action] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_changes] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO