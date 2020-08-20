SELECT        pos.opus_id, per.firstname + ' ' + per.lastname AS Fullname, per.firstname, per.lastname, per.cpr, pos.title AS Position, org.longname AS Orgunit, pos.los_id AS Orgunit_losid_fk, CAST(pos.start_date AS datetime) 
                         AS Ans_dato, CAST(pos.leave_date AS datetime) AS Fra_dato, pos.is_manager, pos.uuid_userref AS User_fk, us.UserId AS samaccount
FROM            pyt.positions AS pos INNER JOIN
                         pyt.persons AS per ON pos.person_ref = per.cpr INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id LEFT OUTER JOIN
                         dbo.Users AS us ON pos.uuid_userref = us.Uuid