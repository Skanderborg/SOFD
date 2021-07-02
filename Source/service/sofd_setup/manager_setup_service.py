from dal.orgunit_repo import Orgunit_repo
from dal.position_repo import Position_repo


class Manager_setup_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def remove_deleted_managers_from_orgunits(self):
        '''
        funktion som fjerner ledere, der ikke længere er ansat i organisationen
        '''
        org_repo = Orgunit_repo(self.constr_lora)
        pos_repo = Position_repo(self.constr_lora)
        orgs = org_repo.get_orgunits('WHERE [manager_opus_id] IS NOT NULL')
        managers = pos_repo.get_positions('WHERE [is_manager] = 1 and [deleted] = 0')
        orgs_to_update = {}
        for los_id in orgs:
            org = orgs[los_id]
            if org.manager_opus_id in managers:
                continue
            else:
                org.manager_opus_id = None
                org.updated = True
                orgs_to_update[los_id] = org
        org_repo.update_orgunits(orgs_to_update)


    def set_orgunit_manager(self):
        '''
        funktion som tilføjer ledere til orgunits, mange orgunits vil ikke have en leder
        '''
        org_repo = Orgunit_repo(self.constr_lora)
        pos_repo = Position_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        managers = pos_repo.get_positions('WHERE [is_manager] = 1 and [deleted] = 0')
        orgs_to_update = {}
        for opus_id in managers:
            manager = managers[opus_id]
            if manager.los_id not in orgs:
                continue
            org = orgs[manager.los_id]
            if org.manager_opus_id == manager.opus_id:
                continue
            else:
                org.manager_opus_id = manager.opus_id
                org.updated = True
                orgs_to_update[org.los_id] = org
        org_repo.update_orgunits(orgs_to_update)
        

    def set_nearest_manager(self):
        '''
        funktion som sætter nærmeste leder på medarbejderne gennem rekursion hvor der ledes op i org hierakiet
        indtil der findes en organisation som har en leder.
        Det her skal køres efter de to andre manager scripts er kørt, fordi det tager udgangspunkt i organsiations
        tabellen og de ledere, som er påtrykt organisations enheder
        '''
        org_repo = Orgunit_repo(self.constr_lora)
        pos_repo = Position_repo(self.constr_lora)
        orgs = org_repo.get_orgunits()
        positions = pos_repo.get_positions('WHERE [deleted] = 0')
        positions_to_update = {}

        for pkey in positions:
            position = positions[pkey]
            # fordi managers ikke skal have sig selv som leder skal vi lige finde det rigtige los_id,
            # hvis du er leder, starter vi på niveauet over dig.
            # dette skal stoppe ved borgmesteren
            los_id_for_recursion = position.los_id

            # hvis der er fucket op i løn, tjekker vi lige at der faktisk er en orgunit
            if los_id_for_recursion not in orgs:
                continue

            if position.is_manager == True:
                org_actual = orgs[los_id_for_recursion]
                if org_actual.niveau > 2:
                    los_id_for_recursion = org_actual.parent_orgunit_los_id

            

            manager_id = Manager_setup_service.get_manager(
                self, los_id_for_recursion, orgs)
            manager_uuid = positions[manager_id].uuid_userref
            if position.manager_opus_id != manager_id or position.manager_uuid_userref != manager_uuid:
                position.manager_opus_id = manager_id
                position.manager_uuid_userref = manager_uuid
                position.updated = True
                positions_to_update[pkey] = position
            else:
                continue
        pos_repo.update_positions(positions_to_update)

    def get_manager(self, los_id, orgs):
        orgunit = orgs[los_id]
        if orgunit.manager_opus_id != None:
            return orgunit.manager_opus_id
        else:
            return Manager_setup_service.get_manager(self, orgunit.parent_orgunit_los_id, orgs)
