# -*- coding:UTF-8 -*-
import platform
from selenium import webdriver


def selenium_driver():
    os_name = platform.system()
    if os_name == 'Windows':
        driver_path = r"D:\Software\ChromePortable\chromedriver.exe"
        print("Windows操作系统，driver路径已配置，路径为：{}".format(driver_path))
        # driver = webdriver.Chrome(executable_path=driver_path)
        return driver_path
    elif os_name == 'Linux':
        print("Linux操作系统，暂未配置driver路径")
    elif os_name == 'Darwin':
        driver_path = r"/Applications/Google Chrome.app/Contents/MacOS/chromedriver"
        print("MacOS操作系统，driver路径已配置，路径为：{}".format(driver_path))
        # driver = webdriver.Chrome(executable_path=driver_path)
        return driver_path
    else:
        print("其他操作系统，暂未配置driver路径")
