USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[Users]    Script Date: 20-08-2020 13:46:48 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Users](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Uuid] [nvarchar](200) NOT NULL,
	[UserId] [nvarchar](50) NOT NULL,
	[Email] [nvarchar](200) NULL,
	[Phone] [nvarchar](200) NULL,
	[Opus_id] [int] NOT NULL,
	[Updated] [bit] NOT NULL,
	[WorkMobile] [nvarchar](50) NULL,
	[Deleted_in_ad] [bit] NOT NULL CONSTRAINT [DF_Users_Deleted_in_ad]  DEFAULT ((0)),
 CONSTRAINT [PK_Users] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [UC_Uuid] UNIQUE NONCLUSTERED 
(
	[Uuid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


