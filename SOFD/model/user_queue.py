import datetime

class User_queue:
    def __init__(self, uuid, opus_id, change_type, change_date):
        self.uuid = uuid
        self.opus_id = opus_id
        self.change_type = change_type
        if change_date != None:
            self.change_date = change_date
        else:
            self.change_date = datetime.datetime.now()