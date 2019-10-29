# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
from fake_useragent import UserAgent
from requests import RequestException
from lxml import etree

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


def get_max_page(data):
    etree_obj = etree.HTML(data)
    page_info = etree_obj.xpath('//div[@class="dxypage clearfix"]/text()')[0]
    page_num = re.findall("页次：.*/(.*?) 每页", page_info)[0]
    page_list = []
    for i in range(1, page_num + 1):
        page_list.append("https://www.jb51.net/list/list_97_{}.htm".format(str(i)))
    return page_list


def parse_page_info(page_url):
    page_resp = request_url(page_url, url_decode="utf8")
    etree_obj = etree.HTML(page_resp)
    page_line_urls = etree_obj.xpath('//div[@class="artlist clearfix"]//dt//a/@href')
    page_line_titles = etree_obj.xpath('//div[@class="artlist clearfix"]//dt//a/text()')
    page_content = []
    for url, title in zip(page_line_urls, page_line_titles):
        info = {"link": url, "title": title, }
        page_content.append(info)


if __name__ == '__main__':
    url = "https://www.jb51.net/list/list_97_1.htm"
    index_data = request_url(url, url_decode="gb2312")
    pagelist = get_max_page(index_data)
