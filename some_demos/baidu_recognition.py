# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  baidu_recognition
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/12/6
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
from aip import AipOcr
from aip import AipNlp

def baidu_online_recognition():
    """百度在线识别"""
    app_id = "17953482"
    api_key = "gKlL51maeDRsLtSO6Ft97tne"
    secret_key = "EuxuLcNh1oYG8zjdhi2RfuaoNgDsMSz8"
    api_ocr = AipOcr(app_id, api_key, secret_key)
    return api_ocr


def field_language_processing():
    """词法分析接口包含了"""
    str_test = "我今天没吃午饭"
    app_id = "17953482"
    api_key = "gKlL51maeDRsLtSO6Ft97tne"
    secret_key = "EuxuLcNh1oYG8zjdhi2RfuaoNgDsMSz8"
    api_nlp = AipNlp(app_id, api_key, secret_key)
    result = api_nlp.lexer(str_test)
    for item in result:
        print(item, result[item])


def get_file_content(filepath):
    """ 读取图片 """
    with open(filepath, 'rb') as fp:
        return fp.read()


def picture_execute():
    """调用入口"""
    filepath = r"G:\v_mzhulliu\test_data\baidu.png"
    api_ocr = baidu_online_recognition()
    image = get_file_content(filepath)
    result = api_ocr.basicGeneral(image)
    ocr_data = result.get("words_result")
    content = " "
    for item in ocr_data:
        content += "{}\n".format(item.get("words").strip())

    print(content)


if __name__ == '__main__':
    field_language_processing()




