# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
#------------------------------------------------------------------------------
# Name:  seliumn_csdn_login
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/10/30
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import time
from selenium import webdriver


driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.find_element_by_id('kw').send_keys("机器学习")#获取输入框
driver.find_element_by_id('su').click()#获取输入框
time.sleep(9)
driver.quit()




