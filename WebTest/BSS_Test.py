# -*- coding:utf-8 -*-
import time
import pytesseract
import random
import os
import sys
import json
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


def code_read(filename='Code_list.txt'):
    """加载组织机构代码证列表"""
    f = open(filename)
    code_list = []
    for line in f.readlines():
        cur_line = line.strip().split()
        code_list.append(cur_line)
    return code_list


def is_exist_element(elem, code='已存在'):
    """判断元素是否存在"""
    try:
        s = driver.find_element_by_xpath(elem)
        if str(s.text).find(code):
            return True
    except NoSuchElementException:
        return False


def sys_login(driver, account, passwd, authCode):
    """登录"""
    driver.find_element_by_id('loginUserCode').clear()
    driver.find_element_by_id('loginPassword').clear()
    driver.find_element_by_name('verifyCode').clear()
    driver.find_element_by_id('loginUserCode').send_keys(account)
    driver.find_element_by_id('loginPassword').send_keys(passwd)
    driver.find_element_by_name('verifyCode').send_keys(authCode)
    driver.find_element_by_xpath('//button[contains(text(),"新版集中集客")]').click()
    """验证是否登录成功"""
    try:
        # driver.switch_to.window(driver.window_handles[1])
        title = driver.find_element_by_xpath(
            '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
        time.sleep(2)
        assert title.find('管理系统')
        print('登录成功')
        customer_manager()
    except IndexError:
        f1 = open('cookie.txt')
        cookie = f1.read()
        cookie = json.loads(cookie)
        for c in cookie:
            driver.add_cookie(c)
        # # 刷新页面
        print('尝试Cookie登录')
        # print(cookie)
        driver.refresh()
        try:
            title = driver.find_element_by_xpath(
                '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
            time.sleep(2)
            assert title.find('管理系统')
            print('登录成功')
            customer_manager()
        except NoSuchElementException:
            print('Cookie登录失败，正在重新登录')
            sys_login(driver, account, passwd, authCode)
    except NoSuchElementException:
        f2 = open('cookie.txt')
        cookie = f2.read()
        cookie = json.loads(cookie)
        for c in cookie:
            driver.add_cookie(c)
        # # 刷新页面
        print('尝试Cookie登录')
        # print(cookie)
        driver.refresh()
        try:
            title = driver.find_element_by_xpath(
                '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
            time.sleep(2)
            assert title.find('管理系统')
            print('登录成功')
            customer_manager()
        except NoSuchElementException:
            print('Cookie登录失败，正在重新登录')
            sys_login(driver, account, passwd, authCode)


def customer_manager():
    """客户资料创建"""
    for code_input in code_read():
        try:
            custumer_click = driver.find_element_by_xpath("//a[contains(@menu_name,'客户中心')]")
            ActionChains(driver).move_to_element(custumer_click).perform()
            driver.find_element_by_xpath("//a[contains(@menu_name,'客户中心')]").find_element_by_xpath(
                "//span[contains(@title,'客户资料管理')]").click()
            time.sleep(5)
            driver.switch_to.frame("2111Iframe")
            """输入参数"""
            sendran = random.randint(1, 1000)
            name_list = ['赵一', '王二', '张三', '李四', '周五']
            sendname = random.randint(0, (len(name_list)) - 1)
            driver.find_element_by_xpath("//a[contains(text(),'政企客户创建')]").click()
            '''获取客户信息'''
            driver.find_element_by_xpath('//*[@id="baseinfo-panel"]/div[1]/form/div[1]/div[1]/div/div[1]/div').click()
            driver.find_element_by_xpath('//li[contains(text(),"统一社会信用代码证书")]').click()
            driver.find_element_by_xpath('//*[@id="baseinfo-panel"]/div[1]/form/div[1]/div[2]/div/div[1]/input').send_keys(code_input)
            driver.find_element_by_xpath('//button[contains(text(),"获取")]').click()
            driver.find_element_by_xpath('//*[@id="jqg1"]').click()
            driver.find_element_by_xpath('/html/body/div[6]/div[3]/button[1]').click()
            driver.find_element_by_xpath('/html/body/div[7]/div[3]/button[1]').click()
            """当前客户信息"""
            cust_name = driver.find_element_by_name('custName').get_attribute('value')
            print('当前客户名称为：' + cust_name + '，统一信用代码证为：' + str(code_input))
            '''基本信息'''
            driver.find_element_by_xpath('//*[@id="custInfoForm"]/div[2]/div[1]/div/div/div/input').click()
            # driver.execute_script('document.getElementsByClassName("ztree")[0].scrollBottom=99999')
            # driver.find_element_by_id('ui-id-40_1_switch').click()
            # driver.find_element_by_id('ui-id-40_2_switch').click()
            driver.find_element_by_id('ui-id-40_68_span').click()
            time.sleep(1)
            if is_exist_element('/html/body/div[5]/div[2]/div'):
                print(str(driver.find_element_by_xpath('/html/body/div[5]/div[2]/div').text) + '，已自动跳过')
                driver.refresh()
                continue
            # hrb_name = driver.find_element_by_id('ui-id-40_68_span')
            # WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(hrb_name))
            # hrb_name.click()
            driver.find_element_by_name('contactPhone').send_keys('16666666666' + str(sendran))
            driver.find_element_by_name('postCode').send_keys('150000')
            driver.find_element_by_name('contactName').send_keys(name_list[sendname] + str(sendran))
            driver.find_element_by_name('callingTypeCode').click()
            driver.find_element_by_link_text("金融业").click()
            driver.find_element_by_link_text("银行").click()
            driver.find_element_by_link_text("主管机构").click()
            driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/button[1]').click()
            '''经办人信息'''
            driver.find_element_by_name('transactorName').send_keys('吴延华')
            driver.find_element_by_xpath('//*[@id="transactorForm"]/div[1]/div[2]/div/div/div').click()
            ActionChains(driver).send_keys(Keys.DOWN).perform()
            time.sleep(1)
            ActionChains(driver).click(on_element=None).perform()
            time.sleep(1)
            # driver.find_element_by_xpath('//*[@id="transactorForm"]/div[1]/div[2]/div/div/div/span[1]').click()
            driver.find_element_by_name("certiAddr").send_keys('这是一条测试地址' + str(sendran))
            driver.find_element_by_name("phone").send_keys('16666666666' + str(sendran))
            driver.find_element_by_name("certiCode").send_keys('371523199206055312')
            driver.find_element_by_xpath('//button[contains(text(),"认证")]').click()
            if is_exist_element('/html/body/div[7]/div[2]/div', '未通过'):
                print(driver.find_element_by_xpath('/html/body/div[7]/div[2]/div').text)
                break
            driver.find_element_by_xpath('/html/body/div[6]/div[3]/button').click()
            # driver.execute_script("document.getElementById('busiLicenseInfo_certFile_filefield').click()")
            '''上传开户证件图像'''
            driver.find_element_by_xpath('//*[@id="creditCertiForm"]/div[4]/div[1]/div/div/div/span[1]/input').click()
            os.system(r'./other/autoupdate.exe')  # 调用外部Auto_it Script进行功能实现
            time.sleep(5)
            '''客户经理信息'''
            # driver.find_element_by_xpath('//*[@id="baseinfo-panel"]/div[5]/div[1]/div/button').click()
            # driver.find_element_by_xpath('//*[@id="managerForm"]/div[2]/div[1]/div/div/input').click()
            # time.sleep(3)
            # driver.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1]/div[2]/div/div/input').send_keys('渠道卡代')
            # driver.find_element_by_xpath('/html/body/div[8]/div[2]/div/div[1]/div[3]/div/div/button').click()
            # driver.find_element_by_xpath('//*[@id="jqg35"]').click()
            # time.sleep(3)
            # driver.find_element_by_xpath('//td[contains(@aria-describedby,"ui-id-43_userOrgName")]').click()
            # driver.find_element_by_xpath('/html/body/div[8]/div[3]/button[1]').click()
            # driver.find_element_by_xpath('/html/body/div[7]/div[3]/button[1]').click()
            '''提交'''
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div/div[2]/div[4]/button[2]').click()
            time.sleep(5)
            if is_exist_element('/html/body/div[7]/div[2]/div'):
                print('该客户已创建，自动跳过')
            else:
                is_exist_element('/html/body/div[6]/div[2]/div', '成功')
                success_code = str(driver.find_element_by_xpath('/html/body/div[6]/div[2]/div').text)
                print(success_code)
        except NoSuchElementException:
            print('识别元素失败,刷新页面')
            driver.refresh()
            continue
        except ElementNotVisibleException:
            print('元素未显示,刷新页面')
            driver.refresh()
            continue
        except WebDriverException:
            print('元素获取错误,刷新页面')
            driver.refresh()
            continue
        print('继续添加下一条，当前时间为：' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        driver.refresh()
    print('所有数据已创建完毕')
    driver.quit()


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
    sys_login(driver, 'jinwf2', 'abc@123', get_auth_code.authCodeText)


class Logger(object):  # Log日志记录
    def __init__(self, filename="Default.log"):
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
    sys.stdout = Logger('客户创建日志.log')
    main()
    # driver.execute_script("window.alert('Selenium执行完毕')")
    # driver.quit()
