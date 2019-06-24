USE [DSA_SOFD_DB]
GO

/******
Object:  Table [OPUS].[OrgUnit]
Script Date: 24-06-2019 15:25:47
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [OPUS].[OrgUnit](
	[lastChanged] [datetime] NULL,
	[id] [int] NULL,
	[client] [smallint] NULL,
	[startDate] [datetime] NULL,
	[endDate] [datetime] NULL,
	[parentOrgUnit] [nvarchar](255) NULL,
	[shortName] [nvarchar](255) NULL,
	[longName] [nvarchar](255) NULL,
	[street] [nvarchar](255) NULL,
	[addressSupplement] [nvarchar](255) NULL,
	[zipCode] [smallint] NULL,
	[city] [nvarchar](255) NULL,
	[phoneNumber] [nvarchar](255) NULL,
	[cvrNr] [int] NULL,
	[eanNr] [bigint] NULL,
	[seNr] [int] NULL,
	[pNr] [int] NULL,
	[costCenter] [bigint] NULL,
	[orgType] [smallint] NULL,
	[orgTypeTxt] [nvarchar](255) NULL,
	[OrgNveau] [int] NULL
) ON [PRIMARY]

GO


