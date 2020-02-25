/****** View som minder om medarbejder overblikket fra den gamle SOFD, der er data felter som vi ikke har, her er der indsat sys_id, men de de skal ud når vi ved de kan  ******/
CREATE VIEW [dbo].[v_sofd_medarbejderoverblik] AS SELECT pos.system_id AS [MedarbejderID],
      pos.opus_id AS [OpusMedarbejderID],
      pos.system_id AS [OpusStillngsID],
      pos.system_id AS [UNICMedarbejderID],
      pos.system_id AS [ADMedarbejderID],
      pos.person_ref AS [CPRnr],
      usr.UserId AS [ADBrugerNavn],
      usr.UserId AS [UNICBrugerID],
      per.firstname AS [Fornavn],
      per.lastname AS [Efternavn],
      usr.Email AS [Mail],
      usr.Phone AS [Tlfnr],
      pos.title AS [StillingBetegnelse],
      pos.system_id AS [Foedselsdag],
      per.[address] AS [PrivatGade],
      per.zipcode AS [PrivatPostnr],
      per.city AS [PrivatBy],
      org.longname AS [ArbejdsstedNavn],
      org.street AS [ArbejdsstedGade],
      org.zipcode as [ArbejdsstedPostnr],
      org.area AS [ArbejdstedBy],
      org.longname AS [LOSOrganisationsenhed],
      pos.los_id AS [LOSOrganisationID],
      pos.manager_opus_id AS [NearmesteLederID],
      pos.manager_uuid_userref AS [NearmesteLederADBrugerID],
      pos.is_manager AS [ErLeder],
      pos.payment_method AS [Ans_forhold],
      pos.start_date AS [Ans_dato],
      pos.leave_date AS [Fratraad_dato],
      pos.kmd_suppid AS [OPUSMedarbejderExtraCiffer],
      pos.payment_method_text AS [Loenkls_tekst],
      pos.weekly_hours_numerator AS [numerator],
      pos.system_id AS [invoiceRecipient],
      pos.system_id AS [invoiceLevel1],
      pos.system_id AS [invoiceLevel1Text],
      pos.system_id AS [invoiceLevel2],
      pos.system_id AS [invoiceLevel2Text],
      org.area AS [Omraede],
      org.area AS [OmraedeID],
      pos.system_id AS [Ferieopdateringsdato],
      pos.system_id AS [Ferietimer_MedLoen],
      pos.system_id AS [Ferie_overfoertetimer]
  FROM [pyt].[positions] as pos
  LEFT join [dbo].[users] as usr on pos.uuid_userref = usr.Uuid
  LEFT join [pyt].[persons] as per on pos.person_ref = per.cpr
  LEFT join [pyt].[orgunits] as org on pos.los_id = org.los_id