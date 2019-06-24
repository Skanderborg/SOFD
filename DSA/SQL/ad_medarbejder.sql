USE [DSA_SOFD_DB]
GO

/****** 
Object:  Table [AD].[Medarbejder]
Script Date: 24-06-2019 15:20:32
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [AD].[Medarbejder](
	[AD_ID] [int] IDENTITY(1,1) NOT NULL,
	[LogonNavn] [nvarchar](50) NULL,
	[Fornavn] [nvarchar](50) NULL,
	[Efternavn] [nvarchar](50) NULL,
	[Mail] [nvarchar](50) NULL,
	[PersonNr] [nvarchar](50) NULL,
	[LokalNr] [nvarchar](50) NULL,
	[TokenID] [nvarchar](50) NULL,
	[MifireID] [nvarchar](50) NULL,
	[SkyPrintPin] [nvarchar](50) NULL,
	[EkstraCiffer] [nvarchar](50) NULL,
	[Afloenningsform] [nvarchar](50) NULL
) ON [PRIMARY]

GO

