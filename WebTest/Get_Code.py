# -*- coding:utf-8 -*-
import os
import time
import random
import sys
import xlrd
import xlwt
from xlutils3.copy import copy
from selenium import webdriver
from PIL import Image
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# 匹配图片，适用有图库（多张）的情况
def match_source(image):
    imagea = Image.open('./pic_code/before_screenshot.png')
    imageb = Image.open('./pic_code/before_screenshot.png')
    imagec = Image.open('./pic_code/before_screenshot.png')
    imaged = Image.open('./pic_code/before_screenshot.png')
    list = [imagea, imageb, imagec, imaged]
    # 通过像素差遍历匹配本地原图
    for i in list:
        pixel1 = image.getpixel((0, 0))
        pixel2 = i.getpixel((0, 0))
        # pixel[0]代表R值，pixel[1]代表G值，pixel[2]代表B值
        if abs(pixel1[0] - pixel2[0]) < 5:
            return i
    return image


# 计算滑块位移距离
def get_diff_location(image1, image2):
    # （0,262）（0,118）为滑块图片区域，可根据实际情况修改
    for i in range(0, 262):
        for j in range(0, 118):
            # 遍历原图与缺口图像素值寻找缺口位置
            if not is_similar(image1, image2, i, j):
                return i
    return -1


# 对比RGB值得到缺口位置
def is_similar(image1, image2, x, y):
    pixel1 = image1.getpixel((x, y + 0))  # 0为偏移量，可设置
    pixel2 = image2.getpixel((x, y))
    # 截图像素也许存在误差，50作为容差范围
    if abs(pixel1[0] - pixel2[0]) >= 50 and abs(pixel1[1] - pixel2[1]) >= 50 and abs(pixel1[2] - pixel2[2]) >= 50:
        return False
    return True


# 滑块移动轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = random.randint(2, 3) / 10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


# 检测表格长度
def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


# 判断元素是否存在
def is_exist_element(elem):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, elem)))
        return True
    except TimeoutException:
        return False


# Log日志记录
class Logger(object):
    def __init__(self, filename="./log/Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


# 计数器
class Counter:
    def __init__(self, start=0):
        self.num = start

    def count(self):
        self.num += 1
        return self.num


# 异常重启
def restart_program():
    time.sleep(1)
    print('模块即将重启，请稍后')
    python = sys.executable
    file_name = sys.argv[0]
    os.execl(python, python, file_name)


# 创建表格
def excel_create(file_path):
    create_num = str(random.randint(1, 1000))
    if os.path.exists('./output_file/Code_data.xls'):
        # 打开已有表
        old = xlrd.open_workbook('./output_file/Code_data.xls', formatting_info=True)
        # 复制原有表
        new = copy(old)
    else:
        # 创建文件
        new = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # 创建Sheet页
    sheet = new.add_sheet(key_value + create_num, cell_overwrite_ok=True)
    # 列名
    table_top_list = ['企业名称', '统一社会信用代码', '注册资本', '工商注册号', '组织机构代码', '注册地址', '行业']
    # 设置表头单元格及文本样式
    style = xlwt.easyxf(
        "font: bold True, colour white, name 微软雅黑;"
        "pattern: pattern solid, fore_colour ocean_blue;"
        "alignment: horizontal center,vertical center;"
        "borders: left 2, right 2, top 2, bottom 2, "
        "left_colour black, right_colour black, top_colour black, bottom_colour black;"
    )
    style1 = xlwt.easyxf(
        "font: bold False, colour black, name 微软雅黑;"
        "pattern: pattern solid, fore_colour ice_blue;"
        "alignment: horizontal center,vertical center;"
        "borders: left 1, right 1, top 1, bottom 1, "
        "left_colour black, right_colour black, top_colour black, bottom_colour black;"
    )
    # 写入表头
    print('开始创建表格')
    for row in range(len(table_top_list)):
        write_data = table_top_list[row]
        sheet.write(0, row, write_data, style)
        data_length_index = len(write_data.encode('utf-8'))  # 获取当前Unicode字符串长度
        """设置单元格宽度"""
        if data_length_index > 10:
            sheet.col(row).width = 256 * (data_length_index + 1)
        print('列名共{0:>2}条,正在添加：{1}'.format(str(len(table_top_list)), write_data))
    # 写入内容
    print('开始写入数据')
    for col in range(len(code_result)):
        write_data = code_result[col]
        print('共计{0:>3}条数据，当前为{1:>3}条，企业名称为：{2}'.format(len(code_result), col + 1, write_data[0]))
        for row in range(len(code_result[col])):
            sheet.write(col + 1, row, write_data[row], style1)
            data_length_index = len(write_data[row].encode('utf-8'))  # 获取当前Unicode字符串长度
            if data_length_index > 10:
                width = int(256 * (data_length_index + 1) * 1.3)
                if width > 65535:
                    sheet.col(row).width = 65535
                else:
                    sheet.col(row).width = width
    # 保存表格
    new.save(file_path)
    print('保存表格成功,当前时间为: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


# 爬虫
def get_code(page_num=1):
    try:
        for select_page in range(page_num):
            # 判断页面结构
            x_path_tree = '//div[contains(@class,"result-list sv-search-container")]'
            search_result_tree = driver.find_elements_by_xpath('{}/div'.format(x_path_tree))
            print('开始查询第{}页数据，当前页共计{}条数据'.format(select_page + 1, len(search_result_tree)))
            for num in range(len(search_result_tree)):
                x_path = '//a[contains(@class,"name select-none")]'
                item = search_result_tree[num].find_elements_by_xpath(x_path)
                if len(item) == 0:
                    x_path = '//a[contains(@class,"name ")]'
                    item = search_result_tree[num].find_elements_by_xpath(x_path)
                # 这里总共有三种实现方式
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, x_path)))
                driver.execute_script("arguments[0].scrollIntoView(true);", item[num])  # 定位当前链接
                # driver.execute_script("document.documentElement.scrollTop=100000")
                ActionChains(driver).move_to_element(item[num]).perform()
                href_get = item[num].get_attribute('href')
                driver.execute_script("window.open('{}')".format(href_get))
                # item[num].click()
                driver.switch_to.window(driver.window_handles[1])
                code_list = []

                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//h1[contains(@class,"name")]')))
                code_name = driver.find_element_by_xpath('//h1[contains(@class,"name")]').text
                code_list.append(code_name)
                try:
                    code_code = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]').text
                    code_list.append(code_code)
                    registered_capital = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/div').get_attribute('title')
                    code_list.append(registered_capital)
                    registration_number = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]').text
                    code_list.append(registration_number)
                    organization_code = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]').text
                    code_list.append(organization_code)
                    address = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[10]/td[2]').text
                    code_list.append(address)
                    industry = driver.find_element_by_xpath(
                        '//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]').text
                    code_list.append(industry)
                    code_result.append(code_list)
                except NoSuchElementException:
                    print('未找到[{}]相关信息，自动跳过'.format(code_name))
                    pass
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                print(code_list)
            if page_num == select_page + 1:
                break
            else:
                page = driver.find_element_by_css_selector(
                    '#web-content > div > div.container-left > div.search-block > '
                    'div.result-footer > div:nth-child(1) > ul > li:nth-child(%s) '
                    '> a' % (select_page + 2))
                page.click()
                time.sleep(3)
        print('查询结束，总计{}页'.format(page_num))
    except TimeoutException:
        print('抓取中断，尝试重新登录')
        if except_check.count() >= 5:
            print('异常次数超限，请检查参数')
            driver.quit()
            return 0
        if len(driver.window_handles) > 0:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        get_code()
    except NoSuchElementException:
        if is_exist_element('//*[@id="hideSearching"]/div/img'):
            print('关键字有误，请检查页面提示信息')
        else:
            print('抓取元素失败')
        time.sleep(5)
        driver.quit()


# 登录
def login(value_key=''):
    print("打开网页")
    driver.get('https://www.tianyancha.com/search?key=%s' % value_key)
    driver.implicitly_wait(5)
    driver.maximize_window()
    # driver.find_element_by_id('home-main-search').send_keys('证券')
    # ActionChains(driver).send_keys(Keys.ENTER).perform()
    # time.sleep(5)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tyc_banner_close"]')))
    driver.find_element_by_xpath('//*[@id="tyc_banner_close"]').click()
    if is_exist_element('//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[1]/div[2]'):
        pwd_login = driver.find_element_by_xpath(
            '//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[1]/div[2]')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[1]/div[2]')))
        # driver.execute_script("arguments[0].click();", pwd_login)
        # ActionChains(driver).move_to_element(pwd_login).click().perform()
        pwd_login.click()
        driver.find_element_by_xpath(
            '//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/input').send_keys('13845072760')
        driver.find_element_by_xpath(
            '//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[2]/div[3]/input').send_keys('wocaonima486')
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        if is_exist_element('/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div[1]'):
            pass
        else:
            driver.find_element_by_xpath(
                '//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[2]/div[5]').click()
        verify_check = True
        while verify_check:
            driver.save_screenshot(r'./pic_code/before.png')
            slideblock = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[2]/div[2]')
            # 鼠标点击圆球不松开
            ActionChains(driver).click_and_hold(slideblock).perform()
            # 将圆球滑至相对起点位置的最右边
            ActionChains(driver).move_by_offset(xoffset=250, yoffset=0).perform()
            # 保存包含滑块及缺口的页面截图
            driver.save_screenshot(r'./pic_code/after.png')
            # 放开圆球
            ActionChains(driver).release(slideblock).perform()
            # 获取验证码元素坐标
            imgElement = driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[1]/div[2]/div[1]')
            imgSize = imgElement.size  # 获取验证码图片的大小
            imgLocation = imgElement.location
            rangle = (int(imgLocation['x']), int(imgLocation['y']), int(imgLocation['x'] + imgSize['width']),
                      int(imgLocation['y'] + imgSize['height']))  # 计算验证码整体坐标
            login = Image.open(r'./pic_code/after.png')
            login1 = Image.open(r'./pic_code/before.png')
            frame = login.crop(rangle)  # 截取验证码图片
            frame1 = login1.crop(rangle)
            frame.save(r'./pic_code/after_screenshot.png')
            frame1.save(r'./pic_code/before_screenshot.png')
            # 打开保存至本地的缺口页面截图
            quekouimg = Image.open(r'./pic_code/after_screenshot.png')
            # 匹配本地对应原图
            sourceimg = match_source(quekouimg)
            # 获取缺口位置
            visualstack = get_diff_location(sourceimg, quekouimg)
            # 获取移动距离loc，2为滑块起点位置
            loc = visualstack - 2
            # 生成拖拽移动轨迹，0为偏移量，是为了模拟滑过缺口位置后返回缺口的情况，可设置
            track_list = get_track(loc + 0)
            time.sleep(2)
            ActionChains(driver).click_and_hold(slideblock).perform()
            time.sleep(0.2)
            # 根据轨迹拖拽圆球
            for track in track_list:
                ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
            # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
            imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
            time.sleep(0.015)
            imitate.perform()
            time.sleep(random.randint(6, 10) / 10)
            imitate.perform()
            time.sleep(0.04)
            imitate.perform()
            time.sleep(0.012)
            imitate.perform()
            time.sleep(0.019)
            imitate.perform()
            time.sleep(0.033)
            ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
            # 放开圆球
            ActionChains(driver).pause(random.randint(6, 14) / 10).release(slideblock).perform()
            time.sleep(2)
            if is_exist_element('//*[@id="web-content"]/div/div[1]/div[2]/div[4]/div'):
                verify_check = False
            else:
                try:
                    driver.find_element_by_xpath('/html/body/div[10]/div[2]/div[2]/div[1]/div[3]/a[1]').click()
                    ActionChains(driver).click(slideblock).perform()
                    time.sleep(3)
                    continue
                except NoSuchElementException:
                    verify_check = False
    time.sleep(3)


# 等于Class.__init__
def main(key='证券', page=1, path='./output_file/Code_data.xls'):
    login(key)
    get_code(page)
    excel_create(path)


if __name__ == '__main__':
    except_check = Counter()
    sys.stdout = Logger('./log/抓取信用代码证日志.log')
    driver = webdriver.Chrome(executable_path=r"D:\Software\ChromePortable\chromedriver.exe")
    driver.implicitly_wait(10)
    driver.minimize_window()
    code_result = []
    # driver.execute_script("var result = prompt('请输入查询关键字');"
    #                       "window.open('https://www.tianyancha.com/search?key='+ result)")
    key_value = input("请输入想查询的关键字：")
    page_value = input("请输入想查询的页数：")
    page_value = int(page_value)
    main(key_value, page_value)
    # driver.execute_script("window.alert('执行完毕')")
    driver.quit()
