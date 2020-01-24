USE [LORA_SOFD]
GO

/****** Object:  Table [pyt].[disabled_orgunits]    Script Date: 16-01-2020 13:59:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [pyt].[disabled_orgunits](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[los_id] [int] NOT NULL,
	[reason] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_disabled_orgunits] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


