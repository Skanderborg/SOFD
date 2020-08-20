SELECT        pos.uuid_userref, per.firstname, per.lastname, us.UserId, us.Email, org.costcenter, pos.los_id, pos.person_ref, pos.manager_uuid_userref, org.longname, unic.unic_userid, pos.deleted, pos.opus_id
FROM            pyt.positions AS pos INNER JOIN
                         pyt.persons AS per ON pos.person_ref = per.cpr LEFT OUTER JOIN
                         dbo.Users AS us ON pos.uuid_userref = us.Uuid INNER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id LEFT OUTER JOIN
                         unic.unic_usernames AS unic ON unic.opus_id = pos.opus_id