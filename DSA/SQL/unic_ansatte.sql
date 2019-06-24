USE [DSA_SOFD_DB]
GO

/******
Object:  Table [UNIC].[Ansatte]
Script Date: 24-06-2019 15:17:05
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [UNIC].[Ansatte](
	[UNICID] [int] IDENTITY(1,1) NOT NULL,
	[brugerID] [nvarchar](255) NULL,
	[cprnr] [nvarchar](255) NULL,
	[initieltPw] [nvarchar](255) NULL,
	[pwStatus] [nvarchar](255) NULL,
	[navn] [nvarchar](255) NULL,
	[fornavn] [nvarchar](255) NULL,
	[efternavn] [nvarchar](255) NULL,
	[skolekomNavn] [nvarchar](255) NULL,
	[mailadresse] [nvarchar](255) NULL,
	[funktionsmarkering] [nvarchar](255) NULL,
	[Institutionsnr] [numeric](20, 0) NULL
) ON [PRIMARY]

GO


