USE [LORA_SOFD]
GO

/****** Object:  Table [kmdl2].[institution_ids]    Script Date: 20-08-2020 13:47:26 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [kmdl2].[institution_ids](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[los_id] [int] NOT NULL,
	[kmdl2_id] [int] NOT NULL,
	[kmdl2_name] [nvarchar](max) NOT NULL,
	[longname] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_institution_ids] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


