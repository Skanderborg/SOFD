from dal.queue_users_repo import Queue_users_repo
from dal.position_repo import Position_repo
from dal.person_repo import Person_repo
from model.queue_user import Queue_user
from model.position import Position
from model.person import Person

class User_queue_service:
    def __init__(self, constr_lora):
        self.constr_lora = constr_lora
        self.position_repo = Position_repo(constr_lora)
        self.person_repo = Person_repo(constr_lora)

    def handle_person_updates(self):
        updated_persons = self.person_repo.get_persons('WHERE [updated] = 1')
        if len(updated_persons) > 0:
            unchanged_positions = self.position_repo.get_positions('WHERE [updated] = 0 and [deleted] = 0')
            positions_to_update = {}
            persons_to_update = {}

            for opus_id in unchanged_positions:
                pos = unchanged_positions[opus_id]
                if pos.cpr in updated_persons:
                    pos.updated = True
                    positions_to_update[opus_id] = pos
                per = updated_persons[pos.cpr]
                per.updated = False
                persons_to_update[pos.cpr] = per
            self.position_repo.update_positions(positions_to_update)
            self.person_repo.update_persons(persons_to_update)

    def handle_deleted_and_updated_positions(self):
        updated_and_deleted_positions = self.position_repo.get_positions('WHERE [updated] = 1 and [deleted] = 1')
        if len(updated_and_deleted_positions) > 0:
            positions_to_update = {}
            for opus_id in updated_and_deleted_positions:
                pos = updated_and_deleted_positions[opus_id]
                pos.updated = False
                positions_to_update[opus_id] = pos
            self.position_repo.update_positions(positions_to_update)


    def run_user_queue_setup(self):
        User_queue_service.handle_person_updates(self)
        User_queue_service.handle_deleted_and_updated_positions(self)
        updated_positions = self.position_repo.get_positions('WHERE [updated] = 1')
        deleted_positions = self.position_repo.get_positions('WHERE [deleted] = 1')
        if len(updated_positions) > 0 or len(deleted_positions) > 0:
            positions_to_update = {}
            queue_items_to_insert = {}
            queue_repo = Queue_users_repo(self.constr_lora)
            i = 0
            for opus_id in updated_positions:
                pos = updated_positions[opus_id]
                queue_item = Queue_user(i, pos.uuid, opus_id, 'Updated', True)
                i+=1
                pos.updated = False
                positions_to_update[opus_id] = pos
                queue_items_to_insert[i] = queue_item
        
            for opus_id in deleted_positions:
                pos = deleted_positions[opus_id]
                queue_item = Queue_user(i, pos.uuid, opus_id, 'Deleted', True)
                i+=1
                queue_items_to_insert[i] = queue_item

            queue_repo.insert_user_queue(queue_items_to_insert)
            self.position_repo.update_positions(positions_to_update)
            






    

