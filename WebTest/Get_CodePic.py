# -*- coding:UTF-8 -*-
import urllib.request
import random
import time
from selenium import webdriver
from WebTest.Selenium_driver_base import selenium_driver


def get_pic(runtime=1):
    image = 'http://10.124.156.55/portal-web/portal/LoginController/vcode.do?1553828805242'
    random_num = random.randint(1, 1000)
    driver = webdriver.Chrome(executable_path=selenium_driver())
    driver.implicitly_wait(10)
    driver.get(image)
    for pic in range(runtime):
        urllib.request.urlretrieve(image, './img/%s-%s.jpg' % (random_num, pic))
        # time.sleep(0.5)
        driver.refresh()
    print('抓取结束，共%s次' % runtime)


if __name__ == '__main__':
    get_code = input('请输入要抓取的图片数量：')
    get_code = int(get_code)
    get_pic(get_code)
