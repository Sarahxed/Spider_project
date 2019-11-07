# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
#------------------------------------------------------------------------------
# Name:  bs4_operate
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/11/4
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import requests
from fake_useragent import UserAgent
from requests import RequestException
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def request_url(url, url_decode="utf8"):
    sess = requests.session()
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        response = sess.get(url=url, headers=headers, verify=False, timeout=20)
        if response.status_code == 200:
            return response.content.decode(url_decode, errors="ignore")
    except RequestException as e:
        print(e)
        print('请求地址出错', url)


def parse_info(data):
    soup = BeautifulSoup(data, 'lxml', from_encoding="utf8")
    spanlist = soup.find_all("span", classmethod="contentpile__content__wrapper__item__info__box__jobname__title")
    print(spanlist)


if __name__ == '__main__':
    resp = request_url(url="https://sou.zhaopin.com/?jl=765&kw=python&kt=3")
    parse_info(resp)
