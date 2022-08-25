class MessageStorage:
    def __init__(self):
        self.storage = {}

    def save_msg(self, uuid, msg):
        self.storage[uuid] = msg

    def get_all_msgs(self):
        msgs = ""
        for k in self.storage.keys():
            msgs += self.storage[k] + "\n"
        return msgs