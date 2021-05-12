USE [LORA_SOFD]
GO

/****** Object:  Table [acubiz].[extra_fields]    Script Date: 12-05-2021 15:35:36 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [acubiz].[extra_fields](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[los_id] [int] NOT NULL,
	[ems] [nvarchar](250) NOT NULL,
	[dim6] [nvarchar](250) NULL,
	[dim7] [nvarchar](250) NULL,
 CONSTRAINT [PK_extra_fields] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


