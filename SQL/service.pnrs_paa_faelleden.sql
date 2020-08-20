USE [LORA_SOFD]
GO

/****** Object:  Table [service].[pnrs_paa_faelleden]    Script Date: 20-08-2020 13:50:37 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [service].[pnrs_paa_faelleden](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[pnr] [bigint] NOT NULL,
 CONSTRAINT [PK_god_ledelse_pnrs] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


