# -*- coding: utf-8 -*-
"""
@Time: 2019/12/4 23:37
@Auth: v_mzhulliu
@File: distributed_server.py
@IDE: PyCharm
@Motto: ABC(Always Be Coding)

"""
import multiprocessing
import multiprocessing.managers
import random
from queue import Queue

task_queue = Queue()  # 发送任务的队列
result_queue = Queue()  # 接收结果的队列


class QueueManger(multiprocessing.managers.BaseManager):
    """BaseManager继承的QueueManger"""
    pass


def return_task_queue():
    global task_queue
    return task_queue


def rerurn_result_queue():
    global result_queue
    return result_queue


def server_execute():
    multiprocessing.freeze_support()
    # 将两个Queue都注册到网络上，callable参数关联了Queue对象
    QueueManger.register("get_task_queue", callable=return_task_queue)
    QueueManger.register("get_result_queue", callable=rerurn_result_queue)
    # 绑定端口，设置验证码
    manager = QueueManger(address=("10.75.22.88", 8888), authkey="123456")
    # 启动Queue
    manager.start()
    # 获得通过网络访问的Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 放任务
    for i in range(10):
        n = random.randint(0, 10)
        print("put task {}".format(n))
        task.put(n)

    # 获取结果
    for j in range(10):
        m = result.get(timeout=10)
        print("get result {}".format(m))
    # 关闭
    manager.shutdown()
    print("manager exit")


if __name__ == '__main__':
    server_execute()