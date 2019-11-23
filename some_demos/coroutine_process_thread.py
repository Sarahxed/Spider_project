# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  coroutine_process_thread
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/11/21
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import asyncio

import aiohttp
import gevent


def coroutine_demo(name, n):
    """python2.x协程调用demo, 不需要等待就顺序进行,需要等待就自动并行"""
    for i in range(n):
        print(name, "等待了", i + 1, "秒")
        # time.sleep(1)
        gevent.sleep(1)  # 不需要等待就顺序进行,需要等待就自动并行


async def get(url):
    """aiohttp发送请求,requests并不支持异步,而aiohttp是支持异步的网络请求的库"""
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    session.close()
    return result


async def request(url):
    result = await get(url)
    return result


def async_tasks(url_list):
    """
    多任务协程调用示例
    :param url_list: 请求列表
    :return:
    """
    tasks = [asyncio.ensure_future(request(url)) for url in url_list]
    loop = asyncio.get_event_loop()  # 建立 loop
    loop.run_until_complete(asyncio.wait(tasks))  # 执行 loop，并且等待所有任务结束
    loop.close()  # 关闭 loop


