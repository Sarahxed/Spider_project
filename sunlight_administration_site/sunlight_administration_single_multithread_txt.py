# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  sunlight_administration_single_multithread_txt
# Purpose: 
# 
# @Author: Sarah
# Copyright:
# Licence:
#
# Created: 2019/12/2
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------

"""阳光问政之问题反馈模块多线程txt存储"""
import queue
import random
import re
import requests
import threading
import time
from fake_useragent import UserAgent
from lxml import etree


def get_record(url):
    """获取总记录条数"""
    sess = requests.session()
    resp = sess.get(url=url, verify=False, timeout=15).content.decode("gb2312", errors="ignore")
    etree_obj = etree.HTML(resp)
    record_list = etree_obj.xpath('//div[@class="pagination"]/text()')
    pat = re.compile("\d+", re.I)
    record = pat.findall(record_list[-1])[0]
    return record


def get_pages(record):
    """生成所有的页码请求链接"""
    record = int(record)
    page_list = []
    if record % 30 == 0:
        for num in range(record // 30 + 1):
            page_list.append("http://wz.sun0769.com/index.php/question/report?page={}".format(num * 30))
    else:
        for num in range(record // 30 + 2):
            page_list.append("http://wz.sun0769.com/index.php/question/report?page={}".format(num * 30))
    return page_list


def parse_page_info(parse_url):
    """解析单个页面数据"""
    try:
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.random}
        sess = requests.session()
        time.sleep(random.randint(1, 10))
        page_text = sess.get(url=parse_url, headers=headers, verify=False, timeout=30).content.decode(
            "gb2312", errors="ignore")
        data_list = []
        etree_obj = etree.HTML(page_text)
        records_list = etree_obj.xpath('//div[@class="newsHead clearfix"]//table[2]//tr')
        for line in records_list:
            record = line.xpath("./td[1]/text()")[0]
            title = line.xpath(".//a[position()<2]//text()")
            title = title[0] + title[1]
            status = line.xpath("./td[4]/span/text()")[0]
            netizen = line.xpath("./td[5]/text()")[0]
            date = line.xpath("./td[6]/text()")[0]
            print(parse_url, record, title, status, netizen, date)
            data_list.append("{}|||{}|||{}|||{}|||{}|||{}\n".format(parse_url, record, title,
                                                                    status, netizen, date))
    except Exception as e:
        print(e)
        print("{}, error".format(parse_url))
    return data_list


def push_data(page_list, queue):
    """将数据压入队列"""
    for page_url in page_list:
        try:
            page_data = parse_page_info(page_url)
            for line in page_data:
                queue.put(line)
        except Exception as e:
            print(page_url, "数据压入失败")
            print(e)
    signal = "end"
    queue.put(signal)


def write2txt(queue, savepath, thread_num):
    """从队列中获取数据存储到txt中"""
    with open(savepath, "a", encoding="utf8", errors="ignore") as f:
        count = 0
        while not queue.empty():
            try:
                data = queue.get(timeout=15)
                if data == "end":
                    count += 1
                    if count == thread_num:
                        break
                f.write(data)
                f.flush()
            except:
                pass


def execute():
    """调用入口"""
    req_url = "http://wz.sun0769.com/html/top/report.shtml"
    savepath = r"G:\v_mzhulliu\测试\阳光问政.txt"
    records = get_record(req_url)
    page_list = get_pages(records)[:4]
    print("记录总数:", records)
    print("请求链接:{}条".format(len(page_list)))
    q = queue.Queue()
    xlist = [[], [], [], [],
             # [], [], [], [], [], []
             ]
    thread_num = len(xlist)
    th_pool = []
    for i in range(len(page_list)):
        xlist[i % thread_num].append(page_list[i])

    for url_list in xlist:
        th = threading.Thread(target=push_data, args=(url_list, q))
        th.start()
        th_pool.append(th)

    write_th = threading.Thread(target=write2txt, args=(q, savepath, thread_num))
    write_th.start()
    th_pool.append(write_th)

    for thd in th_pool:
        thd.join()


def main():
    import fire
    fire.Fire()


if __name__ == '__main__':
    import sys

    sys.exit(main())
