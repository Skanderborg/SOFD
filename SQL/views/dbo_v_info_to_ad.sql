SELECT        pos.uuid_userref AS ad_objectguid, pos.title, pos.opus_id AS employeenumber, pos.los_id AS orgid, org.longname AS department, org.city, org.zipcode AS postalcode, org.street AS streetaddress, 
                         pos.manager_opus_id AS manager_employeenumber, org.area AS company, lois.navn_tekst AS office
FROM            pyt.positions AS pos INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id INNER JOIN
                         LOIS.dbo.CVR_PROD_ENH AS lois ON org.pnr = lois.pnr