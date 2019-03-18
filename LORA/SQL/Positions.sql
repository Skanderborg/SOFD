USE [LORA_SOFD]
GO

/****** Object:  Table [dbo].[Positions]
Script Date: 18-03-2019 10:23:05
Author: Jacob Hansen
******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Positions](
	[System_id] [int] IDENTITY(1,1) NOT NULL,
	[Opus_id] [int] NOT NULL,
	[Name] [nvarchar](max) NOT NULL,
	[Orgunit_losid_fk] [int] NOT NULL,
	[Person_fk] [nvarchar](50) NOT NULL,
	[Ans_dato] [datetime] NOT NULL,
	[Fra_dato] [datetime] NULL,
	[Is_Manager] [bit] NOT NULL,
	[Timetal] [decimal](28, 10) NOT NULL,
	[Pay_method] [int] NOT NULL,
	[Pay_method_text] [nvarchar](max) NOT NULL,
	[Last_changed] [datetime] NOT NULL,
	[User_fk] [nvarchar](200) NULL,
 CONSTRAINT [PK_Positions] PRIMARY KEY CLUSTERED 
(
	[System_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[Positions]  WITH CHECK ADD  CONSTRAINT [FK_Positions_Orgunits] FOREIGN KEY([Orgunit_losid_fk])
REFERENCES [dbo].[Orgunits] ([Los_id])
GO

ALTER TABLE [dbo].[Positions] CHECK CONSTRAINT [FK_Positions_Orgunits]
GO

ALTER TABLE [dbo].[Positions]  WITH CHECK ADD  CONSTRAINT [FK_Positions_Persons] FOREIGN KEY([Person_fk])
REFERENCES [dbo].[Persons] ([Cpr])
GO

ALTER TABLE [dbo].[Positions] CHECK CONSTRAINT [FK_Positions_Persons]
GO

ALTER TABLE [dbo].[Positions]  WITH CHECK ADD  CONSTRAINT [FK_Positions_Users] FOREIGN KEY([User_fk])
REFERENCES [dbo].[Users] ([Uuid])
GO

ALTER TABLE [dbo].[Positions] CHECK CONSTRAINT [FK_Positions_Users]
GO


