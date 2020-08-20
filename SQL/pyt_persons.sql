USE [LORA_SOFD]
GO

/****** Object:  Table [pyt].[persons]    Script Date: 20-08-2020 13:48:17 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [pyt].[persons](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[cpr] [nvarchar](15) NOT NULL,
	[firstname] [nvarchar](max) NOT NULL,
	[lastname] [nvarchar](max) NOT NULL,
	[address] [nvarchar](max) NOT NULL,
	[zipcode] [nvarchar](50) NOT NULL,
	[city] [nvarchar](150) NOT NULL,
	[country] [nvarchar](50) NOT NULL,
	[updated] [bit] NOT NULL,
	[display_firstname] [nvarchar](max) NULL,
	[display_lastname] [nvarchar](max) NULL,
 CONSTRAINT [PK_persons_1] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


