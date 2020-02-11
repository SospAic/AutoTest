# -*- coding:utf-8 -*-
import time
import pytesseract
import random
import os
import sys
import json
import xlrd
import traceback
from selenium import webdriver
from PIL import Image, ImageEnhance
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from WebTest.Selenium_driver_base import selenium_driver
from WebTest.win32_control_simple import upload_win_confirm


def code_read(filename='./input_file/Code_list.txt'):
    """通过TXT文件加载组织机构代码证列表"""
    f = open(filename)
    code_list = []
    for line in f.readlines():
        cur_line = line.strip().split()
        code_list.append(cur_line)
    return code_list


def open_excel(file='./output_file/Code_data.xls'):  # 打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(e)


def excel_by_index(file='./output_file/Code_data.xls', by_index=0):  # 按表的索引读取
    """通过抓取的统一社会信用代码证创建"""
    data = open_excel(file)  # 打开excel文件
    tab = data.sheets()[by_index]  # 选择excel里面的Sheet
    n_rows = tab.nrows  # 行数
    list_create = []  # 创建一个空列表
    for x in range(1, n_rows):  # 第一行为标题（第一行为0），所以从第二行开始
        row = tab.row_values(x, start_colx=1, end_colx=2)
        if row[0] is '-' or None:  # 判断空白或占位符
            continue
        else:
            list_create.append(row[0])
    return list_create


def get_auth_code(driver, codeEelement):
    """获取验证码"""
    driver.save_screenshot('./pic_code/Authcap.png')  # 截取登录页面
    imgSize = codeEelement.size  # 获取验证码图片的大小
    imgLocation = get_auth_code.imgElement.location  # 获取验证码元素坐标
    rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
              int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
    login = Image.open("./pic_code/Authcap.png")
    frame4 = login.crop(rangle)  # 截取验证码图片
    frame4.save('./pic_code/authcode.png')
    authcodeImg = Image.open('./pic_code/authcode.png')
    authCodeText = pytesseract.image_to_string(authcodeImg).strip()
    return authCodeText


def is_exist_element(elem, code='已存在'):
    """判断元素是否存在"""
    try:
        s = driver.find_element_by_xpath(elem)
        if code in str(s.text):
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
            customer_manager()
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
            customer_manager()
        except NoSuchElementException:
            print('Cookie登录失败，正在重新登录')
            sys_login(driver, account, passwd, authCode)
        except FileNotFoundError:
            print('未找到cookie文件,请获取后登录')
            driver.quit()


def customer_manager():
    """客户资料创建"""
    print('加载代码证数据成功，共{}条'.format(len(excel_by_index())))
    for code_input in excel_by_index():  # code_read():
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
            driver.find_element_by_xpath('//*[@id="baseinfo-panel"]/div[1]/form/div[1]/div/div/div[3]/input').send_keys(
                code_input)
            driver.find_element_by_xpath('//button[contains(text(),"获取")]').click()
            # if is_exist_element('/html/body/div[6]/div[2]/div', '未能正确获取'):
            #     warning = driver.find_element_by_xpath('/html/body/div[6]/div[2]/div').text
            #     print(warning)
            #     driver.find_element_by_xpath('/html/body/div[6]/div[3]/button').click()
            #     driver.refresh()
            #     continue
            # driver.find_element_by_xpath('//*[@id="btable_ui-id-40"]').click()
            # driver.find_element_by_xpath('/html/body/div[6]/div[3]/button[1]').click()
            # driver.find_element_by_xpath('/html/body/div[7]/div[3]/button[1]').click()
            """当前客户信息"""
            cust_name = driver.find_element_by_name('custName').get_attribute('value')
            print('当前客户名称为：{}，统一信用代码证为：{}'.format(cust_name, str(code_input)))
            time.sleep(3)
            """基本信息"""
            driver.find_element_by_xpath('//*[@id="custInfoForm"]/div[2]/div[1]/div/div/div/div[2]/input').click()
            time.sleep(1)
            driver.find_element_by_xpath('//a[contains(text(),"哈尔滨")]').click()
            driver.find_element_by_xpath('//a[contains(text(),"哈尔滨市区")]').click()
            driver.find_element_by_xpath('//button[contains(text(),"确定")]').click()
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
            """总部行业分类"""
            driver.find_element_by_name('callingTypeCode').click()
            driver.find_element_by_link_text("金融业").click()
            driver.find_element_by_link_text("银行").click()
            driver.find_element_by_link_text("主管机构").click()
            driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/button[1]').click()
            '''经办人信息'''
            driver.find_element_by_name('transactorName').send_keys('吴余额')
            driver.find_element_by_xpath('//*[@id="transactorForm"]/div[1]/div[2]/div/div/div').click()
            # ActionChains(driver).send_keys(Keys.DOWN).perform()
            # time.sleep(1)
            # ActionChains(driver).click(on_element=None).perform()
            # time.sleep(1)
            driver.find_element_by_xpath('//li[contains(text(),"身份证18位")]').click()
            driver.find_element_by_name("certiAddr").send_keys('这是一条测试地址' + str(sendran))
            driver.find_element_by_name("phone").send_keys('16666666666' + str(sendran))
            driver.find_element_by_name("certiCode").send_keys('371523199206055312')
            driver.find_element_by_xpath('//button[contains(text(),"认证")]').click()
            # if is_exist_element('/html/body/div[4]/div[2]/div', '未通过'):
            #     print(driver.find_element_by_xpath('/html/body/div[4]/div[2]/div').text)
            #     break
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()
            # driver.execute_script("document.getElementById('busiLicenseInfo_certFile_filefield').click()")
            """上传开户证件图像"""
            driver.find_element_by_xpath('//*[@id="creditCertiForm"]/div[4]/div[1]/div/div/div/span[1]/input').click()
            time.sleep(3)
            upload_win_confirm()
            # os.system(r'.\\other\\autoupdate.exe')  # 调用外部Auto_it Script进行功能实现
            time.sleep(2)
            """客户经理信息"""
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
            """提交"""
            driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div/div[2]/div[4]/button[2]').click()
            time.sleep(5)
            if is_exist_element('/html/body/div[5]/div[2]/div'):
                print('该客户已创建，自动跳过')
            else:
                is_exist_element('/html/body/div[4]/div[2]/div', '成功')
                success_code = str(driver.find_element_by_xpath('/html/body/div[4]/div[2]/div').text)
                print(success_code)
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/button').click()
                driver.refresh()
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
    sys_login(driver, '150005', '00-Password', get_auth_code.authCodeText)


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
    driver = webdriver.Chrome(executable_path=selenium_driver())  # Chrome配置参数
    sys.stdout = Logger('./log/客户创建日志.log')
    main()
    # driver.execute_script("window.alert('Selenium执行完毕')")
    driver.quit()
