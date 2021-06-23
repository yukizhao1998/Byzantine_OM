import threading
from MsgTools import MsgTools
import random
import copy
import json


class Lieutenant(threading.Thread):
    def __init__(self, general_num, id, role, queue_list):
        threading.Thread.__init__(self, name='lieutenant_' + str(id))
        self.general_num = general_num
        self.id = id
        self.role = role
        self.queue_list = queue_list
        self.msg_tools = MsgTools(queue_list, self.id)
        self.RETREAT = 0
        self.m = int((general_num - 1) / 3)
        self.msg_tree = {}

    def build_msg_tree(self, root, history_list, current_m):
        if current_m > self.m:
            root["isleaf"] = True
            return
        root['isleaf'] = False
        for id in range(self.general_num):
            if id == self.id or id in history_list:
                continue
            history_list.append(id)
            root[id] = {}
            self.build_msg_tree(root[id], history_list, current_m + 1)
            history_list.pop()
        return root

    @staticmethod
    def find_majority(vote_list):
        dict = {}
        for v in vote_list:
            if not v:
                continue
            if v in dict.keys():
                dict[v] += 1
            else:
                dict[v] = 1
        for v in dict.keys():
            if dict[v] > int(len(vote_list) / 2):
                return v
        return None

    def get_vote(self, root, parent_value):
        if "value" not in root.keys():
            root["value"] = None
        if root == self.msg_tree[0]:
            vote_list = [root["value"]]
        else:
            vote_list = [parent_value]
        if root["isleaf"]:
            root["agreed_value"] = root["value"]
            return root["agreed_value"]
        else:
            for id in range(self.general_num):
                if id in root.keys():
                    agreed_value = self.get_vote(root[id], root["value"])
                    vote_list.append(agreed_value)
            vote = self.find_majority(vote_list)
            if vote:
                root["agreed_value"] = vote
                return vote
            else:
                root["agreed_value"] = 0
                return None

    def get_voting_process(self, root):
        vote_res = dict()
        vote_res[root["agreed_value"]] = [root["value"]]
        if root["isleaf"]:
            return root["agreed_value"]
        else:
            for key in root.keys():
                if key in range(self.general_num):
                    vote_res[root["agreed_value"]].append(self.get_voting_process(root[key]))
        return vote_res

    def run(self):
        self.msg_tree = {0: {}}
        self.build_msg_tree(self.msg_tree[0], [0], 1)
        while True:
            msg = self.msg_tools.receive_msg(5)
            if not msg:
                break
            root = self.msg_tree
            for idx, id in enumerate(msg.get_content()["path"]):
                root = root[id]
            root["value"] = msg.get_content()["value"]
            if len(msg.get_content()["path"]) <= self.m:
                transmit_msg = copy.deepcopy(msg.get_content())
                transmit_msg["value"] = root["value"]
                transmit_msg["path"].append(self.id)
                if self.role == 1:
                    transmit_msg["value"] = random.randint(0, 5)
                    # do not send msg at all
                    if transmit_msg["value"] == 3:
                        continue
                for id in range(self.general_num):
                    if id in transmit_msg["path"]:
                        continue
                    self.msg_tools.send_msg(id, transmit_msg)
        agreed_value = self.get_vote(self.msg_tree[0], None)
        voting_process = self.get_voting_process(self.msg_tree[0])
        print("Lieutenant " + str(self.id) + "'s voting process:" + json.dumps(voting_process) + "\n", end = '')
        # print("Lieutenant " + str(self.id) + "'s message tree:" + json.dumps(self.msg_tree) + "\n", end='')
        if agreed_value:
            self.msg_tools.send_msg(self.general_num, agreed_value)
        else:
            self.msg_tools.send_msg(self.general_num, self.RETREAT)