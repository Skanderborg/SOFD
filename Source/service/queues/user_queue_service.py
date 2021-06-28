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
        updated_positions = position_repo.get_positions('where [updated] = 1 or [deleted] = 1 or [ad_user_deleted] = 1')
        
        if len(updated_positions) > 0:
            positions_to_update = {}
            queue_items_to_insert = {}
            queue_repo = Queue_users_repo(self.constr_lora)
            i = 0
            for opus_id in updated_positions:
                pos = updated_positions[opus_id]
                # deleted vejer tungere end updated, derfor bliver positions, som både er opdaterede og slettede - slettet
                if pos.deleted == True or pos.ad_user_deleted == True:
                    if pos.uuid_userref != None:
                        # hvis der er et uuid, er der en user og så skal STS org opdateres (False)
                        queue_item = Queue_user(i, pos.uuid_userref, opus_id, 'Deleted', False)
                        i+=1
                        queue_items_to_insert[i] = queue_item
                        # nu kan UUID fjernes fra position
                        pos.uuid_userref = None
                        pos.ad_user_deleted = False
                        positions_to_update[opus_id] = pos
                    else:
                        # Hvis der ikke er et uuid, er der ikke en user og så behøves STS ikke at blive opdateret (True) true er lidt snyd, men altså
                        queue_item = Queue_user(i, 'none', opus_id, 'Deleted', True)
                        i+=1
                        queue_items_to_insert[i] = queue_item
                elif pos.updated == True and pos.deleted == False and pos.ad_user_deleted == False:
                    pos.updated = False
                    if pos.uuid_userref != None:
                        queue_item = Queue_user(i, pos.uuid_userref, opus_id, 'Updated', False)
                        i+=1
                        queue_items_to_insert[i] = queue_item
                    positions_to_update[opus_id] = pos
            queue_repo.insert_user_queue(queue_items_to_insert)
            position_repo.update_positions(positions_to_update)

    def clean_user_queue(self):
        '''
            Funktion der ryder op i [pyt].[positions] og [queue].[users_queue] tabellerne, efter synkroniseringerne ud til forskellige systemer er håndteret.

        '''
        queue_repo = Queue_users_repo(self.constr_lora)
        users_and_positions_that_are_handled = queue_repo.get_completed_user_queues()
        pos_repo = Position_repo(self.constr_lora)
        deleted_positions = pos_repo.get_positions('WHERE [Deleted] = 1')
        for key in users_and_positions_that_are_handled:
            pu = users_and_positions_that_are_handled[key]
            # Tjekker om alle synkroniseringer, der skal gennemføres er kørt
            if pu.all_syncs_completed():
                # hvis en bruger er slettet og denne er synkroniseret, kan den nu fjernes fra SOFD'en
                if pu.change_type == 'Deleted':
                    if pu.opus_id in deleted_positions:
                        pos_repo.delete_position(pu.opus_id)
                # sletter item fra køen
                queue_repo.delete_person(pu.system_id)






    

