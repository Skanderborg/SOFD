
class Queue_orgunit:
    def __init__(self, uuid, los_id, change_type, system_id=None, sts_org=False):
        self.system_id = system_id
        self.uuid = uuid
        self.los_id = los_id
        self.change_type = change_type
        self.sts_org = sts_org in ['true', 'True', 1]