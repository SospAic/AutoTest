from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

desired_caps = {'platformName': "Android", 'platformVersion': '4.2.2', 'deviceName': '127.0.0.1:26944',
                'appPackage': 'com.taobao.taobao', 'appActivity': 'com.taobao.tao.welcome.Welcome'}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)          # 建立 session
time.sleep(5)
driver.find_element_by_id("************").click()         # 点击元素
driver.find_element_by_xpath("************").click()      # 点击元素
driver.find_element_by_xpath("************").send_keys(u'123456')   # 发送键值
driver.quit()      # 退出 session