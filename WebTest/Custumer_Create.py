# -*- coding:utf-8 -*-
import time
import pytesseract
import random
import os
import sys
import xlwt
from xlutils3 import copy
from selenium import webdriver
from PIL import Image, ImageEnhance
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def excel_create(filename='集团客户测试结果.xls'):
    # 创建工作簿
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建工作表
    sheet = wbk.add_sheet('集团客户信息', cell_overwrite_ok=True)
    # 表头（table_top_list包含表头每一列的值）
    top_text = '集团客户编码'
    # 写入表头到sheet 1中，第0行第1列
    sheet.write(0, 1, top_text)
    # 表的内容
    Numcatch = driver.find_element_by_xpath("/html/body/div[15]/div[2]/div[2]").text
    sheet.write(1, 1, Numcatch)
    # 保存表格到已有的 excel
    wbk.save(filename)


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


def sys_login(driver, account, passwd, authCode):
    """登录"""
    driver.find_element_by_id('username').send_keys(account)
    driver.find_element_by_id('password').send_keys(passwd)
    driver.find_element_by_id('random').send_keys(authCode)
    driver.find_element_by_id('btn_submit').click()
    time.sleep(6)
    """验证是否登录成功"""
    try:
        driver.switch_to.window(driver.window_handles[1])
        title = driver.find_element_by_id('lightbox').text  # 获取登录标识
        assert title.find('弹出层操作页面')
        print('登录成功')
    except IndexError:
        time.sleep(1)
        driver.find_element_by_id('username').clear()
        driver.find_element_by_id('password').clear()
        driver.find_element_by_id('random').clear()
        driver.find_element_by_id('yzmId').click()
        time.sleep(2)
        main()
        print('尝试重新登录')
    except NoSuchElementException:
        driver.refresh()
        time.sleep(3)
        print('刷新页面')


def customer_manager():
    """集团客户创建"""
    try:
        costumer_id = driver.find_element_by_id('systemUserNameId').text
        assert costumer_id.find('您好')
        print('登录成功')
        """JS点击"""
        # js = 'document.getElementById("contan").click()'
        # driver.execute_script(js)
        """xpath点击"""
        # driver.find_element_by_xpath("//a[text()='客户管理']").click()
        # driver.find_element_by_xpath("//a[contains(text(),'客户管理')]").click()
        # driver.find_element_by_xpath("//a[contains(text(),'客户资料管理')]").click()
        # driver.find_element_by_xpath("//a[contains(text(),'集团客户创建')]").click()
        """菜单点击"""
        driver.find_element_by_link_text('客户管理').click()
        driver.find_element_by_link_text('客户资料管理').click()
        driver.find_element_by_link_text('集团客户创建').click()
        driver.implicitly_wait(10)
        driver.switch_to.frame("50000122")
        """输入参数"""
        sendran = random.randint(1, 1000)
        driver.find_element_by_xpath("//input[contains(@id,'custName')]").send_keys('集客测试' + str(sendran))
        driver.implicitly_wait(10)
        driver.execute_script('document.getElementById("custClassType_combo_arrow").click()')
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        driver.find_element_by_xpath("//input[contains(@id,'areaTreeView_ofShow')]").click()
        driver.find_element_by_xpath("//span[contains(@class,'tree-hit tree-collapsed')]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/table/tbody/tr[3]"
                                     "/td[2]/div/div[1]/ul/li[1]/ul/li[1]/div/span[2]").click()
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div/div[2]/table/tbody/tr[3]"
                                     "/td[2]/div/div[1]/ul/li[1]/ul/li[1]/div/span[3]").click()
        driver.find_element_by_xpath("//span[contains(text(),'三十头镇')]").click()
        driver.find_element_by_xpath("//a[contains(@id,'areaTreeView_saveBlind')]").click()
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustGroupSVO_postAddr')]").send_keys(
            '这是一条测试地址' + str(sendran))
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustomerSVO.contactName')]").send_keys(
            '姓名' + str(sendran))
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustomerSVO.contactPhone')]").send_keys(
            '16666666666' + str(sendran))
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustGroupSVO_postCode')]").send_keys('1500000')
        driver.find_element_by_xpath("//input[contains(@id,'callingTypeCode_ofShow')]").click()
        driver.find_element_by_link_text("金融业").click()
        driver.find_element_by_link_text("银行").click()
        driver.find_element_by_link_text("主管机构").click()
        driver.find_element_by_link_text("确定").click()
        driver.find_element_by_xpath("//input[contains(@id,'SVO_contactName')]").send_keys('客户经理')
        driver.find_element_by_xpath("//span[contains(@id,'SVO_contactPsptTypeCode')]").click()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        driver.find_element_by_xpath("//span[contains(@id,'SVO_contactPsptTypeCode')]").click()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        driver.find_element_by_xpath("//span[contains(@id,'SVO_contactPsptTypeCode')]").click()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustContactSVO_contactPsptId')]").send_keys(
            '352711234' + str(sendran))
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustContactSVO_contactPostAddr')]").send_keys(
            '这是一条测试地址' + str(sendran))
        driver.find_element_by_xpath("//input[contains(@id,'tfFCustContactSVO_contactPhone')]").send_keys(
            '16666666666' + str(sendran))
        driver.find_element_by_link_text("营业执照").click()
        driver.find_element_by_id("busiLicenseInfo.certCode").send_keys('123456789012345' + str(sendran))
        driver.find_element_by_xpath("//span[contains(@class,'l-btn-text')]").click()
        driver.find_element_by_id("busiLicenseInfo.legalName").send_keys('测试' + str(sendran))
        driver.find_element_by_id("busiLicenseInfo.addr").send_keys('这是一条测试地址' + str(sendran))
        # driver.find_element_by_xpath("//input[@value='0']").click()
        driver.find_element_by_xpath("//input[contains(@id,'defaultChk2')]").click()
        radiolist = driver.find_elements_by_xpath("//input[@id='busiLicenseInfo_isCreditCode']")
        for radio in radiolist:
            if radio.get_attribute("value") == "0":
                if not radio.is_selected():
                    radio.click()
        # driver.execute_script("document.getElementById('busiLicenseInfo_certFile_filefield').click()")
        driver.find_element_by_link_text('浏览...').click()
        os.system(r"./other/autoupdate.exe")
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.NUMPAD1).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        driver.find_element_by_xpath("//span[contains(text(),'保 存 ')]").click()

        """通过修改display访问-方法1(示例，方法不适用)"""
        # driver.execute_script("document.getElementById('custClassType').style.display ='block'")
        # Select(driver.find_element_by_xpath("//*[@id='custClassType']")).select_by_value('3')
        """方法2(示例，方法不适用)"""
        # driver.find_element_by_xpath("//*[@id='custClassType_combo_arrow']/option[3]").click()
        print('提交成功')
    except AssertionError:
        driver.refresh()
        time.sleep(2)
        customer_manager()
        print('尝试重新登录')


def main():
    driver.get('http://132.42.43.117/ulp/')
    driver.implicitly_wait(10)
    print('打开页面')
    driver.maximize_window()
    driver.find_element_by_id('random').click()
    get_auth_code.imgElement = driver.find_element_by_id('yzmId')
    get_auth_code.authCodeText = get_auth_code(driver, get_auth_code.imgElement)
    sys_login(driver, '涉密未填写', '涉密未填写', get_auth_code.authCodeText)
    print('正在登录')


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
    driver = webdriver.Chrome(executable_path="D:\\Software\\ChromePortable\\chromedriver.exe")  # Chrome配置参数
    sys.stdout = Logger('./log/集团客户信息测试结果.log')
    main()
    time.sleep(5)
    customer_manager()
    excel_create(r'C:\Users\Administrator\PycharmProjects\AutoTestCustumerList.xls')
    # driver.execute_script("window.alert('Selenium执行完毕')")
    # driver.quit()
