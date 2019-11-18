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

import requests.auth

# 登陆路由器
auth = requests.auth.HTTPBasicAuth("ryan", "password")
req = requests.post(url="http://pythonscraping.com/pages/auth/login.php", auth=auth)
print(req.text)
