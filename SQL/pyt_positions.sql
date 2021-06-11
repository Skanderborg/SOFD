/****** Object:  Table [pyt].[positions]    Script Date: 11-06-2021 12:56:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [pyt].[positions](
	[system_id] [bigint] IDENTITY(1,1) NOT NULL,
	[opus_id] [int] NOT NULL,
	[uuid_userref] [nvarchar](200) NULL,
	[los_id] [int] NOT NULL,
	[person_ref] [nvarchar](15) NOT NULL,
	[kmd_suppid] [int] NOT NULL,
	[title] [nvarchar](250) NOT NULL,
	[position_id] [int] NOT NULL,
	[title_short] [nvarchar](50) NOT NULL,
	[paygrade_title] [nvarchar](250) NOT NULL,
	[is_manager] [bit] NOT NULL,
	[payment_method] [nvarchar](4) NOT NULL,
	[payment_method_text] [nvarchar](50) NOT NULL,
	[weekly_hours_numerator] [decimal](20, 3) NOT NULL,
	[weekly_hours_denominator] [decimal](20, 3) NOT NULL,
	[invoice_recipient] [bit] NOT NULL,
	[pos_pnr] [nvarchar](250) NULL,
	[dsuser] [nvarchar](50) NULL,
	[start_date] [date] NOT NULL,
	[leave_date] [date] NULL,
	[manager_opus_id] [int] NULL,
	[manager_uuid_userref] [nvarchar](200) NULL,
	[updated] [bit] NOT NULL,
	[deleted] [bit] NOT NULL,
	[ad_user_deleted] [bit] NOT NULL,
 CONSTRAINT [PK_positions_1] PRIMARY KEY CLUSTERED 
(
	[system_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [pyt].[positions] ADD  CONSTRAINT [DF_positions_ad_user_deleted]  DEFAULT ((0)) FOR [ad_user_deleted]
GO