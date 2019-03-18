USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[Persons]
Script Date: 18-03-2019 10:22:08
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Persons](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Name] [nvarchar](max) NOT NULL,
	[Cpr] [nvarchar](50) NOT NULL,
	[Firstname] [nvarchar](max) NOT NULL,
	[Lastname] [nvarchar](max) NOT NULL,
	[Private_adr_fk] [int] NOT NULL,
	[Last_changed] [datetime] NOT NULL,
 CONSTRAINT [PK_Persons] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
 CONSTRAINT [UC_Cpr] UNIQUE NONCLUSTERED 
(
	[Cpr] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[Persons]  WITH CHECK ADD  CONSTRAINT [FK_Persons_Adresses] FOREIGN KEY([Private_adr_fk])
REFERENCES [dbo].[Adresses] ([system_id])
GO

ALTER TABLE [dbo].[Persons] CHECK CONSTRAINT [FK_Persons_Adresses]
GO


