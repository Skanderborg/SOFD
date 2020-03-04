-- =============================================
-- Author:		Jacob Hansen
-- Create date: 01-03-2016
-- Description:	Opdaterer Område ID og navn for medarbejdere.
-- =============================================
-- variable
declare @OrgID varchar(50)
declare @ParentLoopID varchar(50)
declare @CurrentOrgNiveau int
declare @OmrådeID varchar(50)
declare @OmrådeName varchar(50)
declare @ParentNiveau int

-- opretter en curser, der kan køres igennem <- henter fra MDM.MedarbejderOplysninger
DECLARE Leder_cursor CURSOR FOR
SELECT DISTINCT LOSOrganisationID FROM MDM.MedarbejderOplysninger

OPEN Leder_cursor

FETCH NEXT FROM Leder_cursor
INTO @OrgID

WHILE @@FETCH_STATUS = 0
BEGIN
	SET @CurrentOrgNiveau = (select OrgNiveau from OPUS.OrgUnit where id = @OrgID)
	
	-- På niveau 4 ligger områder og stabe - hvis en ansats niveau er under 4 er de en del af direktionen
	IF(@CurrentOrgNiveau < 4)
		Begin
			SET @OmrådeID = (select id from OPUS.OrgUnit where longName = 'Direktion')
			SET @OmrådeName = 'Direktion'
		End

	IF(@CurrentOrgNiveau = 4)
		Begin
			SET @OmrådeID = @OrgID
			SET @OmrådeName = (select longName from OPUS.OrgUnit where id = @OrgID)
		End

	IF(@CurrentOrgNiveau > 4)
		Begin
			SET @ParentLoopID = (select parentOrgUnit from OPUS.OrgUnit where id = @OrgID)
			SET @ParentNiveau = (select OrgNiveau from OPUS.OrgUnit where id = @ParentLoopID)
			-- kører så længe ParentNiveau er forskelligt fra 4
			While(@ParentNiveau <> 4)
				Begin
					SET @ParentLoopID = (select parentOrgUnit from OPUS.OrgUnit where id = @ParentLoopID)
					SET @ParentNiveau = (select OrgNiveau from OPUS.OrgUnit where id = @ParentLoopID)
				End
			SET @OmrådeID = @ParentLoopID
			SET @OmrådeName = (select longName from OPUS.OrgUnit where id = @ParentLoopID)
		End
	
	UPDATE MDM.MedarbejderOplysninger set OmraedeID = @OmrådeID, Omraede = @OmrådeName  where LOSOrganisationID = @OrgID

	-- Tager naeste enhed fra curseren
	FETCH NEXT FROM Leder_cursor
		INTO @OrgID
END

CLOSE Leder_cursor
DEALLOCATE Leder_cursor