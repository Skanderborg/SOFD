USE [DSA_SOFD_DB]
GO

/******
Object:  Table [OPUS].[FerieSaldo]
Script Date: 24-06-2019 15:25:04
Author: Jacob Ågård Bennike
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [OPUS].[FerieSaldo](
	[KommuneInfo] [varchar](9) NULL,
	[CPR] [varchar](10) NULL,
	[ANS_FORHOLD_NR] [varchar](1) NULL,
	[Afloenningsform] [varchar](1) NULL,
	[Ferieoptjeningsaar] [varchar](4) NULL,
	[DatoForSaldo] [varchar](10) NULL,
	[FerieTimer_MLoen] [int] NULL,
	[EVTFerieDage_MLoen] [int] NULL,
	[FerieTimer_ULoen] [int] NULL,
	[EVTFerieDage_ULoen] [int] NULL,
	[Overfoertetimer] [int] NULL,
	[EvtOverfoertedage] [int] NULL,
	[FERIEFRIDAGSTIMER_SUM] [int] NULL
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO
