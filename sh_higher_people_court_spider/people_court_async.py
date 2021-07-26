# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""多协程实现上海高级人民法院爬虫案例"""


async def request_parse_info(url, start, end, file):
    """
    :param url: 请求地址
    :param start: 起始页
    :param end: 终止页
    :param file: 存储地址
    :return:
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"F:\python_tool\chromedriver.exe")
    driver.get(url)
    for page in range(start, end + 1):
        js = "javascript:goPage('{}')".format(page)
        driver.execute_script(js)
        await asyncio.sleep(15)
        etree_obj = etree.HTML(driver.page_source)
        print("js is run, page is {}".format(page))
        trs = etree_obj.xpath('//table[@id="report"]//tr[position()>1]')
        for tr in trs:
            courthouse = tr.xpath("./td[1]/font/text()")[0]
            court = tr.xpath("./td[2]/font/text()")[0]
            opening_date = tr.xpath("./td[3]/text()")[0]
            case_number = tr.xpath("./td[4]/text()")[0]
            case_action = tr.xpath("./td[5]/text()")[0]
            department = tr.xpath("./td[6]/div/text()")[0]
            presiding_judge = tr.xpath("./td[7]/div/text()")[0]
            prosecutor = tr.xpath("./td[8]/text()")[0]
            defendant = tr.xpath("./td[9]/text()")[0]
            trial_info = "{}|||{}|||{}|||{}|||{}|||{}|||{}|||{}|||{}".format(courthouse, court, opening_date,
                                                                             case_number, case_action, department,
                                                                             presiding_judge, prosecutor, defendant)
            with open(file, "a", encoding="utf8", errors="ignore") as f:
                f.write(trial_info + "\n")


def start_coroutine(url, savefile):
    """启动多协程爬虫"""
    start = time.time()
    coroutine1 = request_parse_info(url=url, start=1, end=20, file=savefile)
    coroutine2 = request_parse_info(url=url, start=21, end=40, file=savefile)
    coroutine3 = request_parse_info(url=url, start=41, end=60, file=savefile)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        print(asyncio.Task.all_tasks())
        for task in asyncio.Task.all_tasks():
            print(task.cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
    end = time.time()
    print('TIME: ', end - start)


