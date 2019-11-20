# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pyquery

from lxml import etree

"""
提取网页的方式:
    1.xpath
    2.bs4
    3.re
    4.pyquery

"""


def pyquery_demo_one():
    """pyquery提取数据测试"""
    html = '''
    <div>
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
    </div>
    '''
    # pyquery的初始化方式
    pyq_obj_one = pyquery.PyQuery(html)  # 初始化网页字符串
    pyq_obj_two = pyquery.PyQuery(etree.fromstring(html))  # 通过etree初始化
    pyq_obj_three = pyquery.PyQuery("https://www.baidu.com")  # 初始化网址
    pyq_obj_four = pyquery.PyQuery(filename="")  # 初始化文件
    li_list = pyq_obj_one("li").items()
    print(pyq_obj_one(".item-0.active").find("a").attr("href"))
    print(pyq_obj_one(".item-0.active").find("a").text())
    for line in li_list:
        # print(pyq_obj_one(line).text())
        line.text()


def pyquery_request_demo():
    """pyquery请求：POST/GET"""
    pyquery.PyQuery(url="http://www.baidu.com", headers={"user-agent": "pyquery"})
    pyquery.PyQuery(url="https://www.baidu.com/s?", data={"wd": "python"}, method="post", verify=False)

