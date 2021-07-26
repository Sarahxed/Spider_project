# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  stockstar_spider_sql
# Purpose: 
# 
# @Author: Sarah
# Copyright:
# Licence:
#
# Created: 2019/11/4
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import RequestException
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.connect_mysql import MysqlHelper

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def to_configure_mysql():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'xxx',
        'passwd': 'xxx',
        'database': 'stockstar_spider',
        'charset': "utf8"
    }
    # 初始化打开数据库连接
    mydb = MysqlHelper(config)

    # 打印数据库版本
    table_name = 'equity_funds_table'
    attrdict = {
        'fund_code': 'varchar(30)',
        "fund_abbreviation": 'varchar(50) NOT NULL',
        "fund_abbreviation_link": 'varchar(300)',
        'net_unit_value': 'varchar(30)',
        'accumulated_net': 'varchar(30)',
        'daily_growth': 'varchar(30)',
        'daily_growth_rate': 'varchar(30)'
    }
    constraint = 'PRIMARY KEY(`id`)'
    mydb.create_table(table_name, attrdict, constraint)
    return mydb, table_name


def request_url(url, url_decode="utf8"):
    sess = requests.session()
    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent": ua.random}
    try:
        time.sleep(3)
        response = sess.get(url=url, headers=headers, verify=False, timeout=20)
        if response.status_code == 200:
            return response.content.decode(url_decode, errors="ignore")
    except RequestException as e:
        print(e)
        print('请求地址出错', url)


def request_webdriver(url):
    try:
        chrome_options = Options()  # 创建配置对象
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #  驱动的路径
        path = r"D:\webdriver\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        driver.get(url)
        page_source = driver.page_source
        time.sleep(3)
        return page_source
    except Exception as e:
        print("获取页面失败", e)
        return None


def parse_info(data):
    if data:
        soup = BeautifulSoup(data, "lxml", from_encoding="gb2312")
        try:
            mytable = soup.find_all(id="datalist")
            next_link_tag = soup.select("a[class=n]")[0]
            next_link = "http://quote.stockstar.com{}".format(next_link_tag.get("href"))
            next_page = soup.select(".n > em")[0].string
        except Exception as e:
            print(e)
            print("获取下一页链接失败", e)

        try:
            for line in mytable[0].select("tr"):
                insert_found = {}
                insert_found['fund_code'] = line.select('td')[0].get_text()
                insert_found['fund_abbreviation'] = line.select('td')[1].get_text()
                insert_found['fund_abbreviation_link'] = "http://quote.stockstar.com/{}".format(
                    line.select('td')[1].select('a')[0].get("href"))
                insert_found['net_unit_value'] = line.select('td')[2].get_text()
                insert_found['accumulated_net'] = line.select('td')[3].get_text()
                insert_found['daily_growth'] = line.select('td')[4].select('span')[0].get_text()
                insert_found['daily_growth_rate'] = line.select('td')[5].select('span')[0].string

                print("*" * 100)
                print(insert_found)
                time.sleep(2)
                mydb_obj.insert(table_name, params=insert_found)
        except Exception as e:
            print("解析失败", e)
        try:
            if next_link and next_page:
                print("next_link:", next_link)
                time.sleep(6)
                page_data = request_webdriver(next_link)

                parse_info(page_data)
        except Exception:
            print("异常")


if __name__ == '__main__':
    mydb_obj, table_name = to_configure_mysql()
