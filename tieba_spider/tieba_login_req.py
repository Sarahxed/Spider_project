# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  tieba_login_req
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/10/28
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import requests
from fake_useragent import UserAgent
from requests import RequestException
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


def get_baidu_token():
    url_baidu_token = "https://passport.baidu.com/v2/api/?getapi&token=&tpl=tb&subpro=&apiver=v3&tt=1572361542580&class=login&gid=0A3AD77-64D5-4D6C-922C-C1F42B145DD2&loginversion=v4&logintype=dialogLogin&alg=v2&time=1572361543&sig=ajcrREIwVitOTldhSGV6c1B4RkVJQmxVQkVwM2tmVWdaMHVJNkN2U0RESXlMQll5aGtJd2FMYytucE1SUjRIUw%3D%3D&callback=bd__cbs__yimuoo"
    resp = request_url(url=url_baidu_token, url_decode="utf8")
    print(resp)


# 贴吧登入接口
def login_tieba_req(user, pwd, token, gid):
    url_baidu_login = "https://passport.baidu.com/v2/api/?login"
    post_data = {
        "username": user,
        "password": pwd,
        "token": token,
        "gid": gid,
        "tpl": "tb",
        "u": "https://tieba.baidu.com/",
        "staticpage": "https://tieba.baidu.com/tb/static-common/html/pass/v3Jump.html",
        "charset": "UTF-8",
        "callback": "parent.bd__pcbs__zgoxy6"
    }
