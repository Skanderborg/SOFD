
/****** Object:  View [kmdl2].[employees_in_tree]    Script Date: 26-05-2021 09:00:34 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [kmdl2].[employees_in_tree]
AS
SELECT        opus_id, los_id
FROM            pyt.positions AS p
WHERE        (los_id IN
                             (SELECT        los_id
                               FROM            kmdl2.institution_tree))
GO