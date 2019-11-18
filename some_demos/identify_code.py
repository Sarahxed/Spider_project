# !/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

import pytesseract as pt
from PIL import Image

# 测试识别简单验证码
image = Image.open(r"F:\测试数据\1111\9afb9e89af09b5e483e921d189015e51.png")
text = pt.image_to_string(image)
print(text)

p = subprocess.Popen(
    [r"G:\Tesseract\Tesseract-OCR\tesseract.exe", r"F:\测试数据\1111\9afb9e89af09b5e483e921d189015e51.png", "two"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
