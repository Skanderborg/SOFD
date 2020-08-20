USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[feriesaldo]    Script Date: 20-08-2020 13:46:38 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[feriesaldo](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[cpr] [nvarchar](10) NOT NULL,
	[ans_forhold_nr] [nvarchar](1) NOT NULL,
	[afloeningsform] [nvarchar](1) NULL,
	[ferieoptjeningsaar] [nvarchar](4) NULL,
	[dato_for_saldo] [nvarchar](10) NULL,
	[ferietimer_med_loen] [nvarchar](6) NULL,
	[evt_feriedage_med_loen] [nvarchar](6) NULL,
	[ferietimer_uden_loen] [nvarchar](6) NULL,
	[evt_feriedage_uden_loen] [nvarchar](6) NULL,
	[overfoerte_timer] [nvarchar](6) NULL,
	[evt_overfoerte_dage] [nvarchar](6) NULL,
	[feriedagstimer_sum] [nvarchar](7) NULL,
 CONSTRAINT [PK_feriesaldo] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO


