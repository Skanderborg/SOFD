SELECT        per.cpr, per.firstname, per.lastname, per.address, per.zipcode, per.city, per.country, pos.opus_id, pos.uuid_userref, pos.los_id, pos.kmd_suppid, pos.title, pos.position_id, pos.title_short, pos.paygrade_title, 
                         pos.is_manager, pos.payment_method, pos.payment_method_text, pos.weekly_hours_numerator, pos.weekly_hours_denominator, pos.invoice_recipient, pos.pos_pnr, pos.dsuser, pos.start_date, 
                         pos.leave_date, pos.manager_opus_id, pos.manager_uuid_userref, usr.Uuid, usr.UserId, usr.Email, usr.Phone, usr.WorkMobile
FROM            pyt.positions AS pos LEFT OUTER JOIN
                         pyt.persons AS per ON pos.person_ref = per.cpr LEFT OUTER JOIN
                         dbo.Users AS usr ON pos.opus_id = usr.Opus_id