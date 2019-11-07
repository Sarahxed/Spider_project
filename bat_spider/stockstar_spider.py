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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def request_url(url, url_decode="utf8"):
    sess = requests.session()
    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.random}
    try:
        response = sess.get(url=url, headers=headers, verify=False, timeout=20)
        if response.status_code == 200:
            return response.content.decode(url_decode, errors="ignore")
    except RequestException as e:
        print(e)
        print('请求地址出错', url)


def request_webdriver(url):
    chrome_options = Options()  # 创建配置对象
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    #  驱动的路径
    path = r"F:\python_tool\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    driver.get(url)
    page_source = driver.page_source

    print(page_source)
    return page_source
    # soup = BeautifulSoup(data, 'lxml', from_encoding="utf8")
    # print(soup)


def parse_info(data):
    soup = BeautifulSoup(data, "lxml", from_encoding="gb2312")
    print(soup)
    mytable = soup.find_all(id="datalist")
    print(mytable)
    # mytable[0] 第一个表格
    for line in mytable[0].select("tr"):
        for td in line.select("td"):
            # print(td.get_text())
            # print(td.string)




if __name__ == '__main__':
    resp = request_webdriver(url="http://quote.stockstar.com/fund/stock.shtml")
    # resp = request_url(url=r"http://quote.stockstar.com/fund/stock.shtml", url_decode="gb2312")
    parse_info(resp)

