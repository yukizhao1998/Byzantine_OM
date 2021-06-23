import threading
import argparse
from queue import Queue
import os
import random
from Commander import Commander
from Lieutenant import Lieutenant


if __name__ == '__main__':
    for i in range(20):
        general_num = random.randint(2, 12)
        traitor_num = random.randint(0, int((general_num - 1) / 3))
        traitor_list = random.sample(range(general_num), traitor_num)
        general_thread_list = []
        queue_list = [Queue(10000) for _ in range(general_num + 1)]  # the last queue is for main thread
        print("---------- Round " + str(i) + " ----------")
        print("General number:", general_num)
        print("Traitor number:", traitor_num)
        print("Traitor id:", traitor_list)
        for id in range(general_num):
            role = 0
            if id in traitor_list:
                role = 1
            if id == 0:
                general_thread_list.append(Commander(general_num, id, role, queue_list))
            else:
                general_thread_list.append(Lieutenant(general_num, id, role, queue_list))
        for id in range(general_num):
            general_thread_list[id].start()
        for id in range(general_num):
            general_thread_list[id].join()
        print("~~ Result ~~")
        correct_agreed_value = -1
        agreed_value_list = []
        msg_cnt = 0

        while True:
            if queue_list[general_num].empty():
                break
            msg = queue_list[general_num].get()
            msg_cnt += 1
            sender_id = msg.get_sender_id()
            agreed_value = msg.get_content()
            if sender_id not in traitor_list:
                agreed_value_list.append(agreed_value)
                if sender_id == 0:
                    correct_agreed_value = agreed_value
            elif sender_id == 0:
                traitor_commander_send_values = agreed_value
        if correct_agreed_value == -1:
            correct_agreed_value = agreed_value_list[0]
            print("Commander is Traitor, agreed value =", correct_agreed_value)
            print("Commander send values: ", traitor_commander_send_values)
        else:
            print("Commander is honest, agreed value =", correct_agreed_value)
        if msg_cnt != general_num:
            print("Error: should receive %d msg, but receive %d instead!".format(general_num, msg_cnt))
            raise Exception("msg cnt error")
        for value in agreed_value_list:
            if value != correct_agreed_value:
                print("Error: agreed value incorrect!")
                print(correct_agreed_value)
                print(agreed_value_list)
                raise Exception("incorrect value")
        print("Agreement reached!")
