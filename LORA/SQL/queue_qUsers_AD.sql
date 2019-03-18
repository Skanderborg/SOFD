USE [LORA_SOFD]
GO

/****** Object:  Table [queue].[qUsers_AD]
Script Date: 18-03-2019 10:30:35
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [queue].[qUsers_AD](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Uuid] [nvarchar](200) NULL,
	[EmployeeNumber] [int] NOT NULL,
	[Manager] [nvarchar](250) NOT NULL,
	[Company] [nvarchar](250) NOT NULL,
	[Department] [nvarchar](250) NOT NULL,
	[Office] [nvarchar](250) NOT NULL,
	[StreetAddress] [nvarchar](250) NOT NULL,
	[PostalCode] [nvarchar](250) NOT NULL,
	[City] [nvarchar](250) NOT NULL,
	[Title] [nvarchar](250) NOT NULL,
	[Change_type] [nvarchar](10) NOT NULL,
	[Time_added] [datetime] NOT NULL,
 CONSTRAINT [PK_qUsers_AD] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


