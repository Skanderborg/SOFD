USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[Orgunits]
Script Date: 18-03-2019 10:20:47
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Orgunits](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Uuid] [nvarchar](200) NOT NULL,
	[Los_id] [int] NOT NULL,
	[Name] [nvarchar](max) NOT NULL,
	[PayoutUnitUuid] [nvarchar](200) NOT NULL,
	[Created_date] [datetime] NOT NULL,
	[Phone] [nvarchar](200) NOT NULL,
	[Email] [nvarchar](200) NOT NULL,
	[Parent_losid] [int] NOT NULL,
	[Los_short_name] [nvarchar](50) NOT NULL,
	[Adress_ref] [int] NOT NULL,
	[Last_changed] [datetime] NOT NULL,
	[Ean] [bigint] NULL,
	[Pnr] [bigint] NULL,
	[Cost_center] [bigint] NULL,
	[Org_type] [nvarchar](50) NOT NULL,
	[Org_niveau] [int] NOT NULL,
 CONSTRAINT [PK_Orgunits] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [UC_SkortKey] UNIQUE NONCLUSTERED 
(
	[Los_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[Orgunits]  WITH CHECK ADD  CONSTRAINT [FK_Orgunits_Adresses] FOREIGN KEY([Adress_ref])
REFERENCES [dbo].[Adresses] ([system_id])
GO

ALTER TABLE [dbo].[Orgunits] CHECK CONSTRAINT [FK_Orgunits_Adresses]
GO


