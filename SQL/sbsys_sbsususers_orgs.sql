USE [LORA_SOFD]
GO

/****** Object:  Table [sbsys].[sbsysusers_orgs]    Script Date: 20-08-2020 13:50:05 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [sbsys].[sbsysusers_orgs](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[opus_id] [int] NOT NULL,
	[userid] [nvarchar](8) NOT NULL,
	[extensionAttribute9] [nvarchar](max) NOT NULL,
	[extensionAttribute10] [nvarchar](max) NOT NULL,
	[extensionAttribute11] [nvarchar](max) NOT NULL,
	[extensionAttribute12] [nvarchar](max) NOT NULL,
	[extensionAttribute13] [nvarchar](max) NOT NULL,
	[extensionAttribute14] [nvarchar](max) NOT NULL,
	[updated] [bit] NOT NULL,
 CONSTRAINT [PK_sbsysusers_orgs] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


