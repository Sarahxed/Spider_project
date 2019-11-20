# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  request_auth
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/11/15
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import json
import requests
import requests.auth


def request_auth_demo():
    """登陆路由器"""
    auth = requests.auth.HTTPBasicAuth("ryan", "password")
    req = requests.post(url="http://pythonscraping.com/pages/auth/login.php", auth=auth)
    content = req.text


def jsonpath_demo():
    """jsonpath操作"""
    url = "https://www.lagou.com/lbs/getAllCitySearchLabels.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
    json_data = requests.get(url, verify=False, headers=headers).text
    json_tree = json.loads(json_data).get("content")
    print(json_tree)


if __name__ == '__main__':
    jsonpath_demo()
