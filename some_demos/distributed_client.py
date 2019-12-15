# -*- coding: utf-8 -*-
"""
@Time: 2019/12/4 23:37
@Auth: v_mzhulliu
@File: distributed_client.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)

"""
import time
from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass


def client_execute():
    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")
    server_addr = "10.75.22.88"
    m = QueueManager(address=(server_addr, 8888), authkey="123456")
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()
    for i in range(10):
        try:
            n = task.get(timeout=2)
            res = n*10
            time.sleep(1)
            result.put(res)
        except Exception:
            print("queue is empty.")
    print("work exit")


if __name__ == '__main__':
    client_execute()