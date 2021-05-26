/****** View som minder om medarbejder overblikket fra den gamle SOFD, der er data felter som vi ikke har, her er der indsat sys_id, men de de skal ud når vi ved de kan  ******/

/****** Object:  View [dbo].[v_sofd_medarbejderoverblik]    Script Date: 26-05-2021 08:59:21 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****** Script for SelectTopNRows command from SSMS  ******/
CREATE VIEW [dbo].[v_sofd_medarbejderoverblik]
AS
SELECT        pos.system_id AS MedarbejderID, pos.opus_id AS OpusMedarbejderID, pos.system_id AS OpusStillngsID, pos.system_id AS UNICMedarbejderID, usr.Uuid AS ADMedarbejderID, pos.person_ref AS CPRnr, 
                         usr.UserId AS ADBrugerNavn, usr.UserId AS UNICBrugerID, per.firstname AS Fornavn, per.lastname AS Efternavn, usr.Email AS Mail, usr.Phone AS Tlfnr, pos.title AS StillingBetegnelse, 
                         pos.system_id AS Foedselsdag, per.address AS PrivatGade, per.zipcode AS PrivatPostnr, per.city AS PrivatBy, org.longname AS ArbejdsstedNavn, org.street AS ArbejdsstedGade, 
                         org.zipcode AS ArbejdsstedPostnr, org.area AS ArbejdstedBy, org.longname AS LOSOrganisationsenhed, pos.los_id AS LOSOrganisationID, pos.manager_opus_id AS NearmesteLederID, 
                         pos.manager_uuid_userref AS NearmesteLederADBrugerID, pos.is_manager AS ErLeder, pos.payment_method AS Ans_forhold, pos.start_date, pos.leave_date AS Fratraad_dato, 
                         pos.kmd_suppid AS OPUSMedarbejderExtraCiffer, pos.payment_method_text AS Loenkls_tekst, pos.weekly_hours_numerator AS numerator, pos.system_id AS invoiceRecipient, pos.system_id AS invoiceLevel1, 
                         pos.system_id AS invoiceLevel1Text, pos.system_id AS invoiceLevel2, pos.system_id AS invoiceLevel2Text, org.area AS Omraede, org.area AS OmraedeID, pos.system_id AS Ferieopdateringsdato, 
                         pos.system_id AS Ferietimer_MedLoen, pos.system_id AS Ferie_overfoertetimer
FROM            pyt.positions AS pos LEFT OUTER JOIN
                         dbo.Users AS usr ON pos.uuid_userref = usr.Uuid LEFT OUTER JOIN
                         pyt.persons AS per ON pos.person_ref = per.cpr LEFT OUTER JOIN
                         pyt.Orgunits AS org ON pos.los_id = org.los_id
GO