# -*- coding: utf-8 -*-
#
# !/usr/bin/env python
# ------------------------------------------------------------------------------
# Name:  verification_code
# Purpose: 
# 
# @Author: v_mzhulliu
# Copyright: (c) Tencent 2019
# Licence:
#
# Created: 2019/12/9
# Modified:
# Contributors:
#
# ------------------------------------------------------------------------------
import os
import random
import string

from PIL import Image, ImageFilter  # 滤镜
from PIL import ImageDraw
from PIL import ImageFont


class GenerateCode:
    """randomly generated a 6 bit verification code"""

    def __init__(self):
        # 字体路径
        self.font_path = r"F:\python_tool\font\simkai.ttf"
        # 生成验证码位数
        self.text_num = 6
        # 生成图片尺寸
        self.pic_size = (150, 60)
        # 背景颜色 默认为白色
        self.bg_color = (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
        # 字体颜色 默认为黑色
        self.text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # 干扰线颜色 默认为红色
        self.line_color = (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
        # self.line_color = "black"
        # 是否加入干扰线
        self.draw_line = True
        # 加入干扰线条数的上下限
        self.line_number = (1, 4)
        # 是否加入干扰点
        self.draw_points = False
        # 干扰点出现的概率 2%
        self.point_chance = 1

        self.image = Image.new(mode="RGBA", size=(self.pic_size[0], self.pic_size[1]), color=self.bg_color)
        self.font = ImageFont.truetype(self.font_path, 32)
        self.draw = ImageDraw.Draw(self.image)
        self.text = self.gene_text()
        self.save_dir = r"G:\v_mzhulliu\test_data\code2"
        self.code_num = 200

    def gene_text(self):
        """随机生成一个字符串"""
        source = list(string.ascii_letters)
        for i in range(0, 10):
            source.append(str(i))
        text = "".join(random.sample(source, self.text_num))
        print(text)
        return text

    def gene_line(self):
        """随机生成干扰线"""
        begin = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        end = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        self.draw.line([begin, end], fill=self.line_color, width=1)

    def gene_points(self):
        """随机生成干扰点"""
        for w in range(self.pic_size[0]):
            for h in range(self.pic_size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - self.point_chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def gene_code(self):
        """生成验证码图"""
        font_width, font_height = self.font.getsize(self.text)  # 字体的宽度和高度
        self.draw.text(
            xy=((self.pic_size[0] - font_width) / self.text_num, (self.pic_size[1] - font_height) / self.text_num),
            text=self.text,
            font=self.font, fill=self.text_color, font_width=3)

        if self.draw_line:
            n = random.randint(self.line_number[0], self.line_number[1])
            for i in range(n):
                self.gene_line()

        if self.draw_points:
            self.gene_points()

        params = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
        ]
        # 创建扭曲
        self.image = self.image.transform(size=(self.pic_size[0], self.pic_size[1]), method=Image.BILINEAR,
                                          data=params
                                          )
        # 滤镜 边界加强
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        return self.image, self.text

    def execute(self):
        """调用入口"""
        for _ in range(self.code_num):
            gc = GenerateCode()
            image, text = gc.gene_code()
            picture_path = os.path.join(self.save_dir, text + ".png")
            with open(picture_path, "wb") as file:
                image.save(file, format="png")


if __name__ == '__main__':
    x = GenerateCode()
    x.execute()
