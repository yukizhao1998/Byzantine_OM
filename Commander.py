import threading
from MsgTools import MsgTools
import random


class Commander(threading.Thread):
    def __init__(self, general_num, id, role, queue_list):
        threading.Thread.__init__(self, name='commander')
        self.general_num = general_num
        self.id = id
        self.role = role
        self.queue_list = queue_list
        self.msg_tools = MsgTools(queue_list, self.id)
        self.RETREAT = 0
        self.command_number = 0

    def run(self):
        if self.role == 1:
            for general_id in range(1, self.general_num):
                randi = random.randint(0, 5)
                if randi == 5:
                    continue
                self.msg_tools.send_msg(general_id, {"path": [0], "value": randi})
        else:
            self.command_number = random.randint(0, 5)
            for general_id in range(1, self.general_num):
                self.msg_tools.send_msg(general_id, {"path": [0], "value": self.command_number})
        self.msg_tools.send_msg(self.general_num, self.command_number)
        return


