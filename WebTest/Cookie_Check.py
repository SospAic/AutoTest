#!coding=utf-8
import time
from selenium import webdriver
import pickle


class CookieLogin(object):
    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(executable_path=r"D:\Software\ChromePortable\chromedriver.exe")
        self.driver.get(url=url)
        self.set_cookie()
        self.is_login()

    def is_login(self):
        '''判断当前是否登陆'''
        self.driver.refresh()
        html = self.driver.page_source
        if html.find('您好') == -1:  # 利用用户名判断是否登陆
            # 没登录 ,则手动登录
            self.login()
        else:
            # 已经登录 尝试访问搜索记录，可以正常访问
            self.driver.refresh()
            time.sleep(30)  # 延时看效果

    def login(self):
        '''登陆'''
        time.sleep(60)  # 等待手动登录
        self.driver.refresh()
        self.save_cookie()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                cookie_dict = {
                    "domain": ".132.42.43.117/",  # 火狐浏览器不用填写，谷歌要需要
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/ulp/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    CookieLogin('hefei ', 'abc@123')  # 网址，账号，密码
