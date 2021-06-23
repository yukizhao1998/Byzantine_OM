from Message import Message
import queue
import copy


class MsgTools:
    def __init__(self, q_list, id):
        self.q_list = q_list
        self.id = id

    def send_msg(self, receiver_id, content):
        msg = Message(self.id, receiver_id, copy.deepcopy(content))
        self.q_list[receiver_id].put(msg)
        return

    def receive_msg(self, time_out=100):
        try:
            msg = copy.deepcopy(self.q_list[self.id].get(block=True, timeout=time_out))
        except queue.Empty:
            return False
        return msg
