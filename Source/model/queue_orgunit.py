
class Queue_orgunit:
    def __init__(self, uuid, los_id, change_type, system_id=None):
        self.system_id = system_id
        self.uuid = uuid
        self.los_id = los_id
        self.change_type = change_type
