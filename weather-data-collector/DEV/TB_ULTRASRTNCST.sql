USE [KH16]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TB_ULTRASRTNCST](
	[baseDate] [varchar](10) NULL,
	[baseTime] [varchar](10) NULL,
	[category] [varchar](10) NULL,
	[nx] [varchar](10) NULL,
	[ny] [varchar](10) NULL,
	[obsrValue] [varchar](10) NULL,
	[INDATE] [datetime] DEFAULT getdate(),
	[URL] [varchar](255) NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[TB_ULTRASRTNCST] ADD  CONSTRAINT [DF_GETDATE]  DEFAULT (getdate()) FOR [INDATE]
GO


EXEC SP_HELP [TB_ULTRASRTNCST]
