# encoding: utf-8
"""
@author: Sarah
@time: 2020/7/17 23:31
@file: polar_verification_code.py
@desc: B站极验证码破解 仅供参考
"""
import random
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as By

USERNAME = "xxxx"  # 用户名
PASSWORD = "xxxx"  # 密码
THRESHOLD = 60
LEFT = 60
BORDER = 6


class CrackBilibili:
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self) -> None:
        self.browser.get(self.url)
        # 等待直到元素加载出
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        username.send_keys(self.username)
        time.sleep(0.5)
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))
        password.send_keys(self.password)
        time.sleep(0.5)

    def get_login_button(self):
        """
        获取登录按钮
        :return: 按钮对象
        """
        # EC.element_to_be_clickable(): 确认元素是否是可点击的
        return self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))

    def get_screenshot(self):
        """
        获取网页截图(通用)
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_position(self, is_full_bg):
        """
        获取验证码图片位置
        :param is_full_bg: 为True时浏览器会加载完整的验证码图片
        :return: 验证码图片位置
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        fullbg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_fullbg')))
        time.sleep(2)
        if is_full_bg:
            self.browser.execute_script('arguments[0].setAttribute(arguments[1], arguments[2])', fullbg, 'style', '')
        else:
            self.browser.execute_script('arguments[0].setAttribute(arguments[1], arguments[2])', fullbg, 'style',
                                        'display: none')

        print("获取验证码图片位置！")
        location = img.location

        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], \
                                   location['x'] + size['width']

        print('before, top={}, bottom={}, left={}, right={}, size={}'.format(top, bottom, left, right, size))
        top += 70
        bottom += 115
        left += 155
        right += 225
        print('after, top={}, bottom={}, left={}, right={}, size={}'.format(top, bottom, left, right, size))
        return top, bottom, left, right, size

    def get_geetest_image(self, name, is_full_bg):
        """
        获取验证码图片，输入文件名，保存验证码图片
        :param name: 文件名
        :param is_full_bg: True->无缺口组件图片  False->有缺口组件图片
        :return: 验证码图片
        """
        top, bottom, left, right, size = self.get_position(is_full_bg)
        screenshot = self.get_screenshot()
        screenshot.save('bilibili.png')
        captcha = screenshot.crop((left, top, right, bottom))  # 将图片裁剪出来
        size = size["width"] - 1, size["height"] - 1
        captcha.thumbnail(size)
        captcha.save(name)
        return captcha

    def is_pixel_equal(self, image1, image2, x, y):
        """
        对比两张图片，判断2个像素是否相同(通用)
        说明：遍历图片的每个坐标点，获取两张图片对应像素点的RGB数据，
        如果两者的RGB数据在一定范围内，代表两个像素相同，继续对比下一个像素点；
        如果差距超过一定范围，则代表像素点不同，当前位置即为缺口位置。
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        if abs(pixel1[0] - pixel2[0]) < THRESHOLD and abs(pixel1[1] - pixel2[1]) < THRESHOLD and abs(
                pixel1[2] - pixel2[2]) < THRESHOLD:
            return True
        else:
            return False

    def get_gap(self, image_full, image_gap):
        """
        获取缺口的偏移量
        :param image_full: 不带缺口图片
        :param image_gap: 带缺口图片
        :return: 滑块滑动的距离
        """
        for i in range(LEFT, image_full.size[0]):
            for j in range(image_full.size[1]):
                if not self.is_pixel_equal(image_full, image_gap, i, j):
                    return i
        return LEFT

    def get_slider(self):
        """获取滑块"""
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_track(self, distance):
        """
        模拟用户验证行为，计算出移动距离
        说明：拖动过程模拟加速减速过程，前段滑块做匀加速运动，后段滑块做匀减速运动
        公式：滑块加速度a，速度v, 初速度v0，位移x，时间t，关系如下：
             x = v0 * t + 0.5 * a * t * t
             v = v0 + a * t
        :param distance: 滑块移动的距离
        :return: 加速后减速的运动轨迹
        """
        # distance += 20
        forward_tracks = []
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0

        while current < distance:
            if current < mid:
                a = random.randint(2, 3)
            else:
                a = -random.randint(5, 6)
            v0 = v
            v = v0 + a * t
            x = v0 * t + 0.5 * a * t * t
            current += x
            forward_tracks.append(round(x))
        backward_tracks = [-3, -3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        return {'forward_tracks': forward_tracks, 'backward_tracks': backward_tracks}

    def move_to_gap(self, slider, tracks):
        """
        模拟往右滑动到缺口
        :param slider: 滑块
        :param tracks: 轨迹
        :return: None
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 模拟滑块往右滑动，并超出一段距离
        for x in tracks['forward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # time.sleep(0.5)
        # 模拟滑块往左返回滑动靠近缺口
        for x in tracks['backward_tracks']:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()

        ActionChains(self.browser).release().perform()

    def crack(self):
        # 输入账号、密码
        self.open()
        # 点击登录，弹出验证码
        button = self.get_login_button()
        button.click()
        print("点击登录，弹出验证码")
        time.sleep(1)
        # 获取无缺口的验证码图片
        image_full = self.get_geetest_image('bilibili_full.png', True)
        time.sleep(1)
        # 获取有缺口的验证码图片
        image_gap = self.get_geetest_image('bilibili_gap.png', False)
        print("图片保存")
        gap = self.get_gap(image_full, image_gap)
        track = self.get_track(gap - BORDER)
        print("滑块滑动的距离：{}".format(track))
        slider = self.get_slider()
        # 滑动滑块，进行验证
        self.move_to_gap(slider, track)
        time.sleep(5)
        if self.browser.current_url == 'https://www.bilibili.com/':
            print('登录成功！')
        else:
            self.crack()


if __name__ == '__main__':
    crack = CrackBilibili()
    crack.crack()
