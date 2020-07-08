# -*- coding:UTF-8 -*-

import time
from appium import webdriver

desired_caps = {
    "platformName": "iOS",
    "platformVersion": "13.2",
    "deviceName": "iPhone 6",
    "newCommandTimeout": "120",
    "bundleId": "BB.AppiumDemo",
    "noReset": True
}


def test():
    # 获取设备
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    # 获取输入框
    tf = driver.find_element_by_xpath(
        "//XCUIElementTypeApplication[@name='AppiumDemo']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeTextField")
    # 给输入框设置文本
    tf.send_keys("马上点击button")
    # 清除输入框文本
    tf.clear()
    tf.send_keys("3秒后关闭alert")
    # 点击名为 Button 的按钮
    driver.find_element_by_accessibility_id("Button").click()
    # 设置睡眠时间
    time.sleep(3)
    driver.find_element_by_accessibility_id("确定").click()
    tf.clear()
    tf.send_keys("5秒后退出自动化测试")

    time.sleep(5)
    #  退出自动化测试
    driver.quit()


if __name__ == '__main__':
    test()

