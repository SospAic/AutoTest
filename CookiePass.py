#-*- coding:utf-8 -*-
import time
import requests
from selenium import webdriver


def get_system_cookies(url,account,password):
    '''通过request 登陆系统，获取cookie'''
    cookiesList = []
    data = {"username":account,"password":password}
    roomSession  = requests.Session()
    roomSession.post(url,data=data)
    loadCookies = requests.utils.dict_from_cookiejar(roomSession.cookies)
    for cookieName,cookieValue in loadCookies.items():
        cookies = {}
        cookies['name'] = cookieName
        cookies['value'] = cookieValue
        cookiesList.append(cookies)
    return cookiesList


def is_login_status_succeed(driver):
    '''判断是否登陆状态，非登陆状态,通过cookie登陆'''
    loginUrl = 'http://132.42.43.117/ulp/'  #登陆地址
    account = 'hefei'  #账号
    password = 'abc@123'  #密码
    driver.get('http://132.42.43.117/ulp/') #测试是否为登陆状态
    if '新工号' in driver.page_source:  #判断是否登陆为登陆页面
        for cookie in get_system_cookies(loginUrl,account,password): #如果登陆界面获取cookie
            driver.add_cookie(cookie)  #添加cookie ，通过Cookie登陆
    return driver


def request_circle_details(driver,requestUrl):
    '''测试跳转详情'''
    is_login_status_succeed(driver)
    driver.get(requestUrl)
    #verifyField = driver.find_element_by_xpath('/html/body/div/div/div/div/ul').text  #获取页面标题
    try:
        #driver.switch_to.window(driver.window_handles[1])
        verifyField = driver.find_element_by_xpath('//*[@id="login_box"]/div[3]/font').text  # 获取页面标题
        assert verifyField.find('新工号')
        return '测试通过'
    except AssertionError as e:
        return '测试未通过'


'''测试下效果'''
if __name__ == '__main__':
    requestUrl = 'http://132.42.43.117/ulp/'
    driver = webdriver.Chrome(executable_path="D:\\Software\\ChromePortable\\chromedriver.exe")
    driver.maximize_window()
    print (request_circle_details(driver, requestUrl))
    driver.get(requestUrl)
    time.sleep(2)
    driver.quit()
