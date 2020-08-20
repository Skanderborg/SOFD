USE [LORA_SOFD]
GO

/****** Object:  Table [unic].[institutions]    Script Date: 20-08-2020 13:51:09 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [unic].[institutions](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[institution_nr] [nvarchar](50) NOT NULL,
	[institution_name] [nvarchar](250) NOT NULL,
	[los_id] [int] NOT NULL CONSTRAINT [DF_institutions_los_id]  DEFAULT ((0)),
 CONSTRAINT [PK_institutions] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


