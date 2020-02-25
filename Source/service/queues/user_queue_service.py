from dal.queue_users_repo import Queue_users_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo
from model.queue_user import Queue_user
from model.position import Position
from model.person import Person

class User_queue_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora

    def handle_updated_persons(self):
        '''
        Funktion som håndterer opdateringer af personer, hvis de har en IT bruger, skal der oprettes en besked om at deres stilling
        skal opdateres, og dermed komme med i køen.
        Det kan f.eks. være hvis man skifter navn, det skal opdateres i de forskellige IT systemer.

        Vi er kun interserede i de positions, der har en IT bruger fordi der ikke er nogen systemer at opdaterer dem i hvis de ikke har.
        Hvis en position er markeret som slettet eller opdateret i forvejen, ryger den allerede i køen, derfor er der ikke behov for at
        behandle disse
        '''
        person_repo = Person_repo(self.constr_lora)
        updated_persons = person_repo.get_persons('WHERE [updated] = 1')
        if len(updated_persons) > 0:
            positions_to_update = {}
            persons_to_update = {}
            position_repo = Position_repo(self.constr_lora)
            # henter udelukkende de nødvendige positions, se funktion beskrivelse
            poss_with_usr = position_repo.get_positions('WHERE [uuid_userref] IS NOT NULL and [updated] = 0 and [deleted] = 0')
            for opus_id in poss_with_usr:
                pos = poss_with_usr[opus_id]
                if pos.person_ref in updated_persons:
                    pos.updated = True
                    positions_to_update[opus_id] = pos
            position_repo.update_positions(positions_to_update)
            for cpr in updated_persons:
                per = updated_persons[cpr]
                per.updated = False
                persons_to_update[cpr] = per            
            person_repo.update_persons(persons_to_update)

    def update_user_queue(self):
        '''
        Funktion der bygger vores user queue
        '''
        # sørger for at alle person opdateringer er gået igennem før funktionen kører
        User_queue_service.handle_updated_persons(self)
        position_repo = Position_repo(self.constr_lora)
        updated_positions = position_repo.get_positions('where [updated] = 1 or [deleted] = 1')
        
        if len(updated_positions) > 0:
            positions_to_update = {}
            queue_items_to_insert = {}
            queue_repo = Queue_users_repo(self.constr_lora)
            i = 0
            for opus_id in updated_positions:
                pos = updated_positions[opus_id]
                # deleted vejer tungere end updated, derfor bliver positions, som både er opdaterede og slettede - slettet
                if pos.updated == True and pos.deleted == False:
                    pos.updated = False
                    positions_to_update[opus_id] = pos
                    if pos.uuid_userref != None:
                        queue_item = Queue_user(i, pos.uuid_userref, opus_id, 'Updated', True)
                        i+=1
                        queue_items_to_insert[i] = queue_item
                else:
                    if pos.uuid_userref != None:
                        queue_item = Queue_user(i, pos.uuid_userref, opus_id, 'Deleted', True)
                        i+=1
                        queue_items_to_insert[i] = queue_item
                    #position_repo.delete_position(opus_id)
            queue_repo.insert_user_queue(queue_items_to_insert)
            position_repo.update_positions(positions_to_update)





    
