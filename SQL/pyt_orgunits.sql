USE [LORA_SOFD]
GO

/****** Object:  Table [pyt].[Orgunits]    Script Date: 20-08-2020 13:48:05 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [pyt].[Orgunits](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[los_id] [int] NOT NULL,
	[uuid] [nvarchar](200) NULL,
	[last_changed] [date] NOT NULL,
	[longname] [nvarchar](max) NOT NULL,
	[startdate] [date] NOT NULL,
	[enddate] [date] NULL,
	[parent_orgunit_los_id] [int] NOT NULL,
	[parent_orgunit_uuid] [nvarchar](200) NULL,
	[shortname] [nvarchar](250) NOT NULL,
	[street] [nvarchar](max) NOT NULL,
	[zipcode] [nvarchar](16) NOT NULL,
	[city] [nvarchar](max) NOT NULL,
	[phonenumber] [nvarchar](25) NOT NULL,
	[cvr] [nvarchar](max) NULL,
	[ean] [nvarchar](max) NULL,
	[seNr] [nvarchar](max) NULL,
	[pnr] [nvarchar](max) NULL,
	[orgtype] [int] NOT NULL,
	[orgtypetxt] [nvarchar](max) NOT NULL,
	[costcenter] [nvarchar](max) NULL,
	[manager_opus_id] [int] NULL,
	[hierarchy] [nvarchar](25) NOT NULL,
	[niveau] [int] NOT NULL,
	[area] [nvarchar](max) NULL,
	[updated] [bit] NOT NULL,
	[deleted] [bit] NOT NULL,
 CONSTRAINT [PK_Orgunits_1] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


