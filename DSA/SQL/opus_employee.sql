USE [DSA_SOFD_DB]
GO

/******
Object:  Table [OPUS].[Employee]
Script Date: 24-06-2019 15:24:21
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [OPUS].[Employee](
	[employee_Id] [numeric](20, 0) NULL,
	[lastChanged] [datetime] NULL,
	[id] [int] NULL,
	[client] [smallint] NULL,
	[action] [nvarchar](255) NULL,
	[entryDate] [nvarchar](255) NULL,
	[leaveDate] [nvarchar](255) NULL,
	[firstName] [nvarchar](255) NULL,
	[lastName] [nvarchar](255) NULL,
	[addressSupplement] [nvarchar](255) NULL,
	[postalCode] [nvarchar](255) NULL,
	[city] [nvarchar](255) NULL,
	[country] [nvarchar](255) NULL,
	[workPhone] [nvarchar](255) NULL,
	[workContract] [nvarchar](255) NULL,
	[workContractText] [nvarchar](255) NULL,
	[positionId] [int] NULL,
	[position] [nvarchar](255) NULL,
	[positionShort] [nvarchar](255) NULL,
	[invoiceRecipient] [bit] NULL,
	[invoiceLevel1] [nvarchar](255) NULL,
	[invoiceLevel1Text] [nvarchar](255) NULL,
	[invoiceLevel2] [nvarchar](255) NULL,
	[invoiceLevel2Text] [nvarchar](255) NULL,
	[productionNumber] [nvarchar](255) NULL,
	[isManager] [bit] NULL,
	[superiorLevel] [smallint] NULL,
	[subordinateLevel] [smallint] NULL,
	[orgUnit] [int] NULL,
	[email] [nvarchar](255) NULL,
	[userId] [nvarchar](255) NULL,
	[payGradeText] [nvarchar](255) NULL,
	[numerator] [decimal](28, 10) NULL,
	[denominator] [decimal](28, 10) NULL,
	[initialEntry] [nvarchar](255) NULL,
	[entryIntoGroup] [nvarchar](255) NULL
) ON [PRIMARY]

GO


