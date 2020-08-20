USE [LORA_SOFD]
GO

/****** Object:  Table [ad].[org_uiid]    Script Date: 20-08-2020 13:46:07 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [ad].[org_uiid](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[OrgOpusID] [nvarchar](max) NOT NULL,
	[orguuid] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_org_uiid] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


