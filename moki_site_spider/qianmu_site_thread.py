#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : qianmu_site_thread.py
@time  : 2020/9/5 20:20
"""
from queue import Queue
from threading import Thread

import requests
from fake_useragent import UserAgent
from lxml import etree

"""迁木站点-多线程实现爬取学校详情"""


def fetch(url):
    """请求并下载入口"""
    ua = UserAgent().random
    resp = requests.get(url, headers={'User-Agent': ua})
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.text


def parse_university(url):
    """请求并解析详情页"""
    data = {}
    selector = etree.HTML(fetch(url))
    name = selector.xpath('//h1[@class="wikiTitle"]/text()')
    if name:
        data['name'] = name[0]
        table = selector.xpath('//div[@class="infobox"]//table')
        if table:
            table = table[0]
            if table is not None:
                keys = table.xpath('.//td[1]/p/text()')
                cols = table.xpath('.//td[2]')
                values = [" ".join([i.strip() for i in (col.xpath('.//text()'))]) for col in cols]
                if len(keys) != len(values):
                    return None
                data.update(zip(keys, values))
                return data
    return None


def storage_data(data):
    if data:
        print(data)


def download(link_queue):
    while True:
        link = link_queue.get()
        data = parse_university(link)
        storage_data(data)
        if link == "exit":
            break
        link_queue.task_done()
        print("队列剩余请求数：{}".format(link_queue.qsize()))


if __name__ == '__main__':
    link_queue = Queue()
    thread_num = 10
    threat_pool = []
    url = "http://www.qianmu.org/ranking/1528.htm"
    resp = fetch(url)
    selector = etree.HTML(resp)
    links = selector.xpath('//div[@class="rankItem"][2]//tr/td[2]/a/@href')
    for link in links:
        link_queue.put(link)

    for num in range(thread_num):
        t = Thread(target=download, args=(link_queue,))
        t.start()
        threat_pool.append(t)

    # 阻塞队列，直到队列为空
    link_queue.join()
    # 向队列发送信号，通知线程退出
    for i in range(thread_num):
        link_queue.put('exit')

    # 退出线程
    for j in threat_pool:
        j.join()
