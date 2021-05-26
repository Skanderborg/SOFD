/****** Object:  Table [kmdl2].[institution_ids]    Script Date: 26-05-2021 09:05:44 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [kmdl2].[institution_ids](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[los_id] [int] NOT NULL,
	[kmdl2_id] [int] NOT NULL,
	[kmdl2_name] [nvarchar](max) NULL,
	[sync_children] [bit] NOT NULL,
 CONSTRAINT [PK_institution_ids] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [kmdl2].[institution_ids] ADD  CONSTRAINT [DF_institution_ids_cjildren]  DEFAULT ((1)) FOR [sync_children]
GO


