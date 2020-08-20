SELECT        org.Name AS orgenhed, pos.Name AS stilling, pos.User_fk, org.Pnr
FROM            dbo.Positions AS pos INNER JOIN
                         dbo.Orgunits AS org ON pos.Orgunit_losid_fk = org.Los_id
WHERE        (pos.Is_Manager = 1) AND (org.Pnr IN
                             (SELECT        pnr
                               FROM            service.pnrs_paa_faelleden AS fal)) AND (pos.User_fk IS NOT NULL)