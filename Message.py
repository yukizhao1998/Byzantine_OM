class Message:
    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.content = content
        self.receiver_id = receiver_id

    def get_sender_id(self):
        return self.sender_id

    def get_receiver_id(self):
        return self.receiver_id

    def get_content(self):
        return self.content

    def get_msg_type(self):
        return self.msg_type
