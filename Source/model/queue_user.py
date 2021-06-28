class Queue_user:
    def __init__(self, system_id, uuid, opus_id, change_type, sts_org, mox_acubiz=False):
        self.system_id = system_id
        self.uuid = uuid
        self.opus_id = opus_id
        self.change_type = change_type
        self.sts_org = sts_org in ['true', 'True', 1]
        self.mox_acubiz = mox_acubiz in ['true', 'True', 1]

    def all_syncs_completed(self):
        return self.sts_org == True and self.mox_acubiz == True
