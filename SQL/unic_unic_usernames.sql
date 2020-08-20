USE [LORA_SOFD]
GO

/****** Object:  Table [unic].[unic_usernames]    Script Date: 20-08-2020 13:51:18 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [unic].[unic_usernames](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[cpr] [nvarchar](10) NOT NULL,
	[unic_userid] [nvarchar](50) NOT NULL,
	[institution_nr] [nvarchar](50) NOT NULL,
	[opus_id] [int] NULL,
 CONSTRAINT [PK_unic_usernames] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


