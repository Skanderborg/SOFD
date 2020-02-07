class Sbsys_extension:
    def __init__(self, opus_id, userid):
        self.extensionAttributes = []
        self.opus_id = opus_id
        self.userid = userid

    def add_extensionAttriute(self, extensionAttribute):
        self.extensionAttributes.append(extensionAttribute)
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__