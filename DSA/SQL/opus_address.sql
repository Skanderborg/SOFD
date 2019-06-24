USE [DSA_SOFD_DB]
GO

/******
Object:  Table [OPUS].[Address]
Script Date: 24-06-2019 15:22:37
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [OPUS].[Address](
	[protected] [bit] NULL,
	[text] [nvarchar](255) NULL,
	[employee_Id] [numeric](20, 0) NULL
) ON [PRIMARY]

GO


