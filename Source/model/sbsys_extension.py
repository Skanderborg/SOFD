class Sbsys_extension:
    def __init__(self, opus_id, samaccount):
        self.extensionAttributes = []
        self.opus_id = opus_id
        self.samaccount = samaccount

    def add_extensionAttriute(self, los_id, extensionAttribute):
        self.extensionAttributes.append([los_id, extensionAttribute])