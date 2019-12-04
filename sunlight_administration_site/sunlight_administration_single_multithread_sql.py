# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  sunlight_administration_single_multithread_sql
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/11/27
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------

"""阳光问政之问题反馈模块多线程mysql存储"""
import random
import re
import threading
import time

import requests
from fake_useragent import UserAgent
from lxml import etree

from sunlight_administration_site.data_storage import Spider

spider = Spider()


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
    for url in parse_url:
        try:
            ua = UserAgent(verify_ssl=False)
            headers = {"User-Agent": ua.random}
            sess = requests.session()
            page_text = sess.get(url=url, headers=headers, verify=False, timeout=30).content.decode(
                "gb2312", errors="ignore")
            time.sleep(random.randint(1, 10))
            # print(url)
            etree_obj = etree.HTML(page_text)
            records_list = etree_obj.xpath('//div[@class="newsHead clearfix"]//table[2]//tr')
            for line in records_list:
                record = line.xpath("./td[1]/text()")[0]
                title = line.xpath(".//a[position()<2]//text()")
                title = title[0] + title[1]
                status = line.xpath("./td[4]/span/text()")[0]
                netizen = line.xpath("./td[5]/text()")[0]
                date = line.xpath("./td[6]/text()")[0]
                print(url, record, title, status, netizen, date)
                spider.insert(url=url, record=record, title=title, status=status, netizen=netizen, time=date)
        except Exception as e:
            print(e)
            print("{}, error".format(url))


def execute():
    """调用入口"""
    req_url = "http://wz.sun0769.com/html/top/report.shtml"
    records = get_record(req_url)
    page_list = get_pages(records)
    print("请求链接:{}条".format(len(page_list)))
    xlist = [[], [], [], [], [], [], [], [], [], []]
    thread_num = len(xlist)
    thread_list = []
    for i in range(len(page_list)):
        xlist[i % thread_num].append(page_list[i])

    for j in range(thread_num):
        print("线程请求数量", len(xlist[j]))
        th = threading.Thread(target=parse_page_info, args=(xlist[j],))
        th.start()
        thread_list.append(th)

    for thd in thread_list:
        thd.join()


if __name__ == '__main__':
    execute()
