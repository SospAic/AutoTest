# -*- coding:utf-8 -*-
import time
import xlwt
import sys
import os
from selenium import webdriver
from WebTest.Selenium_driver_base import selenium_driver


def excel_create(file_path):  # 创建表格
    """声明条件变量"""
    row = 1
    col = 0
    col_top_length = list()
    col_table_length = list()
    table_top_list = driver.find_elements_by_css_selector(
        "#main-container>div.main-right.right.split-containe>div.mr-content>div.table-container>"
        "div>div.table_container_fix>table>thead>tr>th>strong")
    # search_data = driver.find_elements_by_xpath("//*[@id='table_main']/tbody/tr[1]/td")
    search_result_tree = driver.find_elements_by_xpath("//*[@id='table_main']/tbody/tr")
    matrix = [[0 for i in range(len(table_top_list))] for i in range(len(search_result_tree))]
    # search_check = search_data[5].is_displayed()  # 调试用
    """变更Displayed属性"""
    # driver.execute_script("document.getElementById('initIndexCharts').style.display ='block'")
    # print(search_data[4].get_attribute('innerText'), search_data[5].text, search_check)  # 调试用
    """创建工作簿"""
    wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    """创建工作表"""
    sheet_title = driver.find_element_by_id("treeZhiBiao_1_span").text
    sheet = wbk.add_sheet(sheet_title, cell_overwrite_ok=True)
    """设置表头单元格及文本样式"""
    style = xlwt.easyxf(
        "font: bold True, colour white, name 微软雅黑;"
        "pattern: pattern solid, fore_colour ocean_blue;"
        "alignment: horizontal center,vertical center;"
        "borders: left 2, right 2, top 2, bottom 2, "
        "left_colour black, right_colour black, top_colour black, bottom_colour black;"
    )
    """数据列表样式"""
    style1 = xlwt.easyxf(
        "font: bold False, colour black, name 微软雅黑;"
        "pattern: pattern solid, fore_colour ice_blue;"
        "alignment: horizontal center,vertical center;"
        "borders: left 1, right 1, top 1, bottom 1, "
        "left_colour black, right_colour black, top_colour black, bottom_colour black;"
    )
    """写入表头"""
    print('开始抓取')
    for row in range(row, (len(table_top_list) + 1)):
        write_data = table_top_list[row - 1].get_attribute('innerText')
        sheet.write(col, (row - 1), write_data, style)
        data_length_index = len(write_data.encode('utf-8'))  # 获取当前Unicode字符串长度
        """设置单元格宽度"""
        if data_length_index > 10:
            sheet.col(row - 1).width = 256 * (data_length_index + 1)
        col_top_length.append(data_length_index)  # 保存每组长度至数组
        # print(data_length_index)  # 调试用
        row += 1
        # print(col_top_length)  # 调试用
        print('数据头为' + str(len(table_top_list)) + '条,当前数据为\t' + write_data)
        """滚屏抓取隐藏元素"""
        if row == 6:
            driver.execute_script('document.getElementsByClassName("table_container_main")[0].scrollLeft=10000')
            # time.sleep(1)  # 休眠1秒
            """重置滚动条"""
        elif row == (len(table_top_list) + 1):
            row = 1
            driver.execute_script('document.getElementsByClassName("table_container_main")[0].scrollLeft=0')
            break
    clo_length_b = col_top_length[:]  # 获取数据头每组长度
    print("=" * max(col_top_length) * 4)
    """添加表内容"""
    for row in range(row, (len(table_top_list) + 1)):
        try:
            check_data = search_result_tree[col]. \
                find_elements_by_xpath("//*[@id='table_main']/tbody/tr[%i]/td" % row)
            for col in range(col, (len(check_data) + 1)):
                insert_data = check_data[col].get_attribute('innerText')
                sheet.write(row, col, insert_data, style1)
                """获取Unicode长度"""
                data_length = len_byte(insert_data)  # len(insert_data.encode('utf-8'))
                """判断数据表长度是否大于数据头长度，取长值"""
                col_compare = clo_length_b[col]
                if col_compare > data_length:
                    data_length = col_compare
                if data_length > 10:
                    sheet.col(col).width = 256 * (data_length + 1)
                """将所有字符串长度保存至多维数组"""
                matrix[row - 1][col] = len(insert_data.encode('utf-8'))
                col_table_length = matrix[row - 1]
                # print(col_table_length)  # 调试用
                # print(matrix)  # 调试用
                # print(data_length)  # 调试用
                print('总计' + str((len(check_data)) * (len(search_result_tree))) + '条,当前数据为\t' + insert_data)
                col += 1
                if col == 6:
                    driver.execute_script(
                        'document.getElementsByClassName("table_container_main")[0].scrollLeft=10000')
                    driver.implicitly_wait(2)
                    # time.sleep(1)  # 休眠1秒
                elif col == len(check_data):
                    col = 0
                    driver.execute_script('document.getElementsByClassName("table_container_main")[0].scrollLeft=0')
                    break
            if row == (len(search_result_tree) + 1):
                break
            print("=" * max(col_table_length))  # 输出分隔符
        except ValueError as e:
            print(e)
            break
        except IndexError as e:
            print(e)
            break

    """保存表格到Excel"""
    wbk.save(file_path)
    print('保存表格成功,当前时间为: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def len_byte(value):  # 检测表格长度
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def main():
    print("打开网页")
    driver.get('http://data.stats.gov.cn/')
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.find_element_by_link_text('月度数据').click()
    time.sleep(3)
    print('搜索成功')


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
    # path = os.path.abspath(os.path.dirname(__file__))
    # type = sys.getfilesystemencoding()
    sys.stdout = Logger('./log/测试结果.log')
    driver = webdriver.Chrome(executable_path=selenium_driver())
    main()
    excel_create(r'./output_file/Total_data.xls')
    # driver.execute_script("window.alert('执行完毕')")
    driver.quit()
