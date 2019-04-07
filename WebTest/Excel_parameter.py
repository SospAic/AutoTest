# encoding: utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import xlrd


def open_excel(file='./input_file/参数列表.xls'):  # 打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(e)


def excel_by_index(file='./input_file/参数列表.xls', colindex=0, by_index=0):  # 按表的索引读取
    data = open_excel(file)  # 打开excel文件
    tab = data.sheets()[by_index]  # 选择excel里面的Sheet
    n_rows = tab.nrows  # 行数
    n_cols = tab.ncols  # 列数
    col_name = tab.row_values(colindex)  # 第0行的值
    list_create = []  # 创建一个空列表
    for x in range(1, n_rows):  # 第一行为标题（第一行为0），所以从第二行开始
        row = tab.row_values(x)
        if row:
            app = {}  # 创建空字典
            for y in range(0, n_cols):
                app[col_name[y]] = row[y]
            list_create.append(app)
    return list_create


def login():
    list_data = excel_by_index(r"./input_file/参数列表.xls", 0)
    # print(list_data) #  调试用
    if len(list_data) <= 0:
        assert 0, u"Excel数据异常"

    for i in range(0, len(list_data)):

        assert "百度" in driver.title
        print(list_data[i]['用户名'] + ": " + str(list_data[i]['密码']))
        # 搜索开始
        driver.find_element_by_id('kw').clear()
        driver.find_element_by_id('kw').send_keys(list_data[i]['用户名'] + '+')
        driver.find_element_by_id('kw').send_keys(str(list_data[i]['密码']))
        driver.find_element_by_id("su").click()
        driver.implicitly_wait(10)
        time.sleep(2)


if __name__ == '__main__':
    # driver = webdriver.Firefox(firefox_binary=r"D:\Software\Mozilla Firefox\firefox.exe",
    #                           executable_path=r"D:\Software\Mozilla Firefox\geckodriver.exe")  # Firefox配置参数
    driver = webdriver.Chrome(executable_path=r"D:\Software\ChromePortable\chromedriver.exe")
    driver.get("https://www.baidu.com/")
    login()
    driver.quit()
