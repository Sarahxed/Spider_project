# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
#------------------------------------------------------------------------------
# Name:  alibaba_job_spider
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/10/31
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import time

import requests
from fake_useragent import UserAgent
from requests import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver

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


def get_alibaba_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    page_source = driver.page_source
    time.sleep(5)
    next_elem = driver.find_element_by_xpath('//div[@class="pagination"]//li[last()]//a')
    next_elem.click()
    time.sleep(20)
    print(page_source)



if __name__ == '__main__':
    get_alibaba_page(url="https://job.alibaba.com/zhaopin/positionList.htm?spm=a2obv.11410899.0.0.55ef6c614l92f9")
