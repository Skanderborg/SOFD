USE [DSA_SOFD_DB]
GO

/******
Object:  Table [OPUS].[Function]
Script Date: 24-06-2019 15:25:25
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [OPUS].[Function](
	[startDate] [datetime] NULL,
	[endDate] [datetime] NULL,
	[artId] [smallint] NULL,
	[orgDaekning] [nvarchar](255) NULL,
	[artText] [nvarchar](255) NULL,
	[members] [int] NULL,
	[roleId] [int] NULL,
	[roleText] [nvarchar](255) NULL,
	[employee_Id] [numeric](20, 0) NULL
) ON [PRIMARY]

GO


