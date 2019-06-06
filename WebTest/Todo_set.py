# -*- coding:utf-8 -*-
import time
import pytesseract
import random
import os
import sys
import json
import traceback
import pdb
from selenium import webdriver
from PIL import Image, ImageEnhance
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def get_auth_code(driver, codeEelement):
    """获取验证码"""
    driver.save_screenshot('./pic_code/Authcap.png')  # 截取登录页面
    imgSize = codeEelement.size   # 获取验证码图片的大小
    imgLocation = get_auth_code.imgElement.location  # 获取验证码元素坐标
    rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']), int(imgLocation['y']+imgSize['height']))  # 计算验证码整体坐标
    login = Image.open("./pic_code/Authcap.png")
    frame4 = login.crop(rangle)   # 截取验证码图片
    frame4.save('./pic_code/authcode.png')
    authcodeImg = Image.open('./pic_code/authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText


def sys_login(driver, account, passwd, authCode):
    """登录"""
    driver.find_element_by_id('loginUserCode').clear()
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_name('verifyCode').clear()
    driver.find_element_by_id('loginUserCode').send_keys(account)
    driver.find_element_by_id('loginPassword').send_keys(passwd)
    driver.find_element_by_name('verifyCode').send_keys(authCode)  # 调试后修改回authCode
    driver.find_element_by_xpath('//button[contains(text(),"新版集中集客")]').click()
    """验证是否登录成功"""
    try:
        # driver.switch_to.window(driver.window_handles[1])
        title = driver.find_element_by_xpath(
            '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
        time.sleep(2)
        assert title.find('管理系统')
        print('登录成功')
        todo_check(runtime)
    except IndexError:
        try:
            f1 = open('./input_file/cookie.txt')
            cookie = f1.read()
            cookie = json.loads(cookie)
            for c in cookie:
                driver.add_cookie(c)
            # # 刷新页面
            print('尝试Cookie登录')
            # print(cookie)
            driver.refresh()
            title = driver.find_element_by_xpath(
                '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
            time.sleep(2)
            assert title.find('管理系统')
            print('登录成功')
            todo_check(runtime)
        except NoSuchElementException:
            print('Cookie登录失败，正在重新登录')
            sys_login(driver, account, passwd, authCode)
        except FileNotFoundError:
            print('未找到cookie文件,请获取后登录')
            driver.quit()
    except NoSuchElementException:
        try:
            f2 = open('./input_file/cookie.txt')
            cookie = f2.read()
            cookie = json.loads(cookie)
            for c in cookie:
                driver.add_cookie(c)
            # # 刷新页面
            print('尝试Cookie登录')
            # print(cookie)
            driver.refresh()
            title = driver.find_element_by_xpath(
                '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
            time.sleep(2)
            assert title.find('管理系统')
            print('登录成功')
            todo_check(runtime)
        except NoSuchElementException:
            print('Cookie登录失败，正在重新登录')
            sys_login(driver, account, passwd, authCode)
        except FileNotFoundError:
            print('未找到cookie文件,请获取后登录')
            driver.quit()


def todo_check(runtime):
    """处理待办"""
    try:
        todo_click = driver.find_element_by_xpath("//a[contains(@menu_name,'系统管理')]")
        ActionChains(driver).move_to_element(todo_click).perform()
        driver.find_element_by_xpath('//span[@title="待办/待阅管理"]').click()
        time.sleep(5)
    except ElementNotVisibleException:
        print('元素未显示,刷新页面')
        driver.refresh()
        time.sleep(3)
        todo_click = driver.find_element_by_xpath("//a[contains(@menu_name,'系统管理')]")
        ActionChains(driver).move_to_element(todo_click).perform()
        driver.find_element_by_xpath('//span[@title="待办/待阅管理"]').click()
        time.sleep(5)
    for num in range(runtime):
        try:
            todo_list = driver.find_elements_by_xpath('//tr[@class="jqgrow row-striped"]')
            todo_list[0].find_element_by_xpath('//span[text()="处理"]').click()
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
            driver.find_element_by_name('auditContent').send_keys('测试通过')
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/form/div[2]/div/div/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[3]/div[3]/button').click()
            print('已处理{}条数据'.format(num + 1))
            time.sleep(2)
        except NoSuchElementException:
            print('识别元素失败,刷新页面')
            traceback.print_exc()
            driver.refresh()
            time.sleep(3)
            todo_click = driver.find_element_by_xpath("//a[contains(@menu_name,'系统管理')]")
            ActionChains(driver).move_to_element(todo_click).perform()
            driver.find_element_by_xpath('//span[@title="待办/待阅管理"]').click()
            time.sleep(5)
            continue
        except ElementNotVisibleException:
            driver.find_element_by_xpath('//*[@id="taskDetailDiv"]/div/div/div[3]/div/div/div/button').click()
            driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[2]/div[3]/button').click()
            time.sleep(2)
            print('被驳回待办，已关单')
            continue
        except WebDriverException:
            print('元素获取错误,刷新页面')
            traceback.print_exc()
            driver.refresh()
            time.sleep(3)
            todo_click = driver.find_element_by_xpath("//a[contains(@menu_name,'系统管理')]")
            ActionChains(driver).move_to_element(todo_click).perform()
            driver.find_element_by_xpath('//span[@title="待办/待阅管理"]').click()
            time.sleep(5)
            continue
        print('继续处理下一条，当前时间为：' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print('所有数据已处理完毕')


def main():
    driver.get('http://10.124.156.55/portal-web/index.jsp')
    print('打开页面')
    driver.implicitly_wait(10)
    driver.maximize_window()
    time.sleep(2)
    get_auth_code.imgElement = driver.find_element_by_class_name('js-vcode-img')
    get_auth_code.authCodeText = get_auth_code(driver, get_auth_code.imgElement)
    print('验证码为：' + get_auth_code.authCodeText)
    print('正在登录')
    sys_login(driver, '150001', 'abc@2468', get_auth_code.authCodeText)
    todo_check(runtime)


class Logger(object):  # Log日志记录
    def __init__(self, filename="./log/Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


if __name__ == '__main__':
    # driver = webdriver.Firefox(firefox_binary=r"D:\Software\Mozilla Firefox\firefox.exe",
    #                           executable_path=r"D:\Software\Mozilla Firefox\geckodriver.exe")  # Firefox配置参数
    driver = webdriver.Chrome(executable_path=r"D:\Software\ChromePortable\chromedriver.exe")  # Chrome配置参数
    sys.stdout = Logger('./log/待办处理日志.log')
    driver.minimize_window()
    runtime = input('请输入要处理多少条数据：')
    runtime = int(runtime)
    main()
    # driver.execute_script("window.alert('Selenium执行完毕')")
    driver.quit()
