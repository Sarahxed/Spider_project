# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  tieba_index_req
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/10/21
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import re

import requests
from fake_useragent import UserAgent
from requests import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def request_url(url, url_decode="utf8"):
    sess = requests.session()
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        response = sess.get(url=url, headers=headers, verify=False, timeout=20)
        if response.status_code == 200:
            return response.content.decode(url_decode)
    except RequestException as e:
        print(e)
        print('请求地址出错', url)


def get_tieba_list(search_name):
    sess = requests.session()
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    base_url = "http://tieba.baidu.com/f?&kw={}".format(search_name)
    try:
        response = sess.get(url=base_url, headers=headers, verify=False, timeout=20)
        if response.status_code == 200:
            resp = response.content.decode("utf8")

            restr_posts = '<span class=\"card_infoNum\">(.*?)</span>'  # 帖子数
            regex_posts = re.compile(restr_posts)
            posts_number = eval("".join(regex_posts.findall(resp)).replace(",", ""))
            restr_like = '<span class=\"card_menNum\">(.*?)</span>'  # 关注数
            regex_likes = re.compile(restr_like)
            likes_number = eval("".join(regex_likes.findall(resp)).replace(",", ""))
            return posts_number, likes_number
    except RequestException as e:
        print(e)
        print('请求地址出错', base_url)


# 匹配所有页码的所有帖子链接
def get_urls_from_page(search_name):
    url_list = []
    posts_number, likes_number = get_tieba_list(search_name)
    if posts_number % 50 == 0:
        pages = posts_number // 50
    else:
        pages = posts_number // 50 + 1
    for i in range(pages):
        page_url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(search_name, str(i * 50))
        print(page_url)
        # url_list.append(page_url)
        page_resp = request_url(url=page_url)
        page_restr = 'href="(/p/\d+)'
        page_regex = re.compile(page_restr)
        info = page_regex.findall(page_resp)
        for p in info:
            p = "{}{}".format("http://tieba.baidu.com", p)
            url_list.append(p)
    return url_list


# 获取每页上的所有邮箱账号
def get_email_from_page(url):
    pagedata = request_url(url, url_decode="utf8")
    print(pagedata)
    restr = r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})"  # 正则表达式，（）只要括号内的数据
    regex = re.compile(restr, re.IGNORECASE)
    emaillist = regex.findall(pagedata)
    print(emaillist)
    return emaillist


if __name__ == '__main__':
    get_email_from_page("http://tieba.baidu.com/p/6305824032")
