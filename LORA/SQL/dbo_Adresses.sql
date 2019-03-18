USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[Adresses]
Script Date: 18-03-2019 10:18:27 
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Adresses](
	[system_id] [int] IDENTITY(1,1) NOT NULL,
	[gade] [nvarchar](max) NOT NULL,
	[postnr] [int] NOT NULL,
	[by] [nvarchar](max) NOT NULL,
 CONSTRAINT [PK_Adresses] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO


