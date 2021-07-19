# -*- coding:utf-8 -*-
import os
import re
import time
from datetime import datetime

from xlutils3.copy import copy
import xlrd
import xlwt


index_name = 'test'
index_list = [
    '主要硬件',
    ['No.', '类型', '品牌', '型号', '数量（个）', '维护方式', '所在机房', '已运行时间（天）', '控制'],
    [['1', 'PTN设备', '华为', 'CX600系列、ATN系列', '3334', '远程', '哈尔滨市区', '1781'], ['存在问题 ： 未发现问题', '问题详细 ：']],
    '安全系统',
    ['No.', '品牌/研发方', '型号', '数量（个）', '维护方式', '所在机房', '已运行时间（天）', '控制'],
    [['1', '无', '无', '0', '远程', '无', '0'], ['存在问题 ： 未发现问题', '问题详细 ：']],
    '基础软件',
    ['No.', '类型', '厂商', '当前版本', '套数', '维护方式', '所在机房', '已运行时间（天）', '所在设备', '是否为正版软件', '控制'],
    [['1', '操作系统', '微软', 'win7', '2', '本地', '哈尔滨市尚志局4楼网管', '1781', '联想电脑', '是'], ['存在问题 ：', '问题详细 ：']],
    '应用软件',
    ['No.', '名称', '研发方', '当前版本', '套数', '维护方式', '所在机房', '已运行时间（天）', '所在设备', '控制'],
    [['1', '网管u2000软件', '第三方研发', 'U2000 V200R018C50CP2003', '2', '本地', '哈尔滨尚志局网管4楼', '1781', '联想电脑'],
     ['存在问题 ：', '问题详细 ：']],
    '公网IP地址段',
    ['No.', 'IP分类', 'IP地址段', 'IP地址描述', '控制'],
    [['没有数据']],
    '主要协议和端口',
    ['No.', '端口', '端口描述', '对应IP', '控制'],
    [['没有数据']]
]


class Excel:
    def __init__(self, filepath='./output_file/'):
        """ 设置表头单元格及文本样式 """
        self.data_length = 0
        self.style = xlwt.easyxf(
            "font: bold True, colour white, name 微软雅黑;"
            "pattern: pattern solid, fore_colour ocean_blue;"
            "alignment: horizontal center,vertical center;"
            "borders: left 2, right 2, top 2, bottom 2, "
            "left_colour black, right_colour black, top_colour black, bottom_colour black;"
        )
        self.style1 = xlwt.easyxf(
            "font: bold False, colour black, name 微软雅黑;"
            "pattern: pattern solid, fore_colour ice_blue;"
            "alignment: horizontal center,vertical center;"
            "borders: left 1, right 1, top 1, bottom 1, "
            "left_colour black, right_colour black, top_colour black, bottom_colour black;"
        )
        self.filepath = filepath
        now = datetime.now()
        # create_num = str(random.randint(1, 1000))
        self.create_date = now.strftime('%Y-%m-%d_%H%M%S')  # 创建日期，可配合随机码使用
        self.create_name = '{}test{}.xls'.format(self.filepath, self.create_date)

    def index_create(self, sheet_title, content_title=None, content=None):
        """ 创建目录 """
        if os.path.exists(self.create_name):
            # 打开已有表
            old = xlrd.open_workbook(self.create_name, formatting_info=True)
            # 复制原有表
            new = copy(old)
        else:
            # 创建文件
            new = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建Sheet页
        sheet = new.add_sheet(sheet_title, cell_overwrite_ok=True)
        # 写入表头
        print('创建目录')
        for row in range(len(content_title)):
            write_data = content_title[row]
            sheet.write(0, row, write_data, self.style)
            data_length_index = len(write_data.encode('utf-8'))  # 获取当前Unicode字符串长度
            """设置单元格宽度"""
            if data_length_index > 10:
                sheet.col(row).width = 256 * (data_length_index + 1)
            print('列名共{0:>2}条,正在添加：{1}'.format(str(len(content_title)), write_data))
        # 写入内容
        col = 0
        row = 0
        for total in range(len(content)):
            write_data = content[total]
            print('共计{0:>3}条用例，当前为{1:>3}条：{2}'.format(len(content), row + 1, write_data))
            sheet.write(col + 1, row, write_data, self.style1)
            data_length_index = len(str(write_data).encode('utf-8'))  # 获取当前Unicode字符串长度
            if row == 2 or row == 3:  # 请求和返回值过长，设固定值
                sheet.col(row).width = 6000
            elif row == 13:
                sheet.col(row).width = 15000
            else:
                if data_length_index > 10:
                    width = int(256 * (data_length_index + 1) * 1.1)
                    if width > 65535:
                        sheet.col(row).width = 65535
                    else:
                        sheet.col(row).width = width
            row += 1
            if row == 8:
                col += 1
                row = 0
        # 保存表格
        try:
            new.save(self.create_name)
            print('目录创建成功，当前时间为： ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except PermissionError:
            print('文件未关闭，保存失败，请关闭文件后重试')
            pass

    def excel_create(self, content_title, content):
        """ 创建详情 """
        if os.path.exists(self.create_name):
            # 打开已有表
            old = xlrd.open_workbook(self.create_name, formatting_info=True)
            # 复制原有表
            new = copy(old)
        else:
            # 创建文件
            new = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建Sheet页
        sheet = new.add_sheet(content_title, cell_overwrite_ok=True)
        print('创建{}详情'.format(content_title))
        # 写入表头
        sheet.write(0, 0, content_title, self.style)
        # 写入内容
        row = 0
        total = 1
        for index in content:
            print('共计{0:>3}条信息，当前为{1:>3}条：{2}'.format(len(content), total, index))
            col = 0
            # 识别标题
            if type(index) == str:
                sheet.write(row, col, index, self.style)
                data_length_index = len(index.encode('utf-8'))  # 获取当前Unicode字符串长度
                if data_length_index > 10:
                    width = int(256 * (data_length_index + 1) * 1.3)
                    if width > 65535:
                        sheet.col(row).width = 65535
                    else:
                        sheet.col(row).width = width
                col += 1
            # 识别详细数据
            elif type(index) == list:
                for aa in index:
                    # 子标题
                    if type(aa) == str:
                        sheet.write(row, col, aa, self.style)
                        data_length_index = len(aa.encode('utf-8'))  # 获取当前Unicode字符串长度
                        if data_length_index > 10:
                            width = int(256 * (data_length_index + 1) * 1.3)
                            if width > 65535:
                                sheet.col(row).width = 65535
                            else:
                                sheet.col(row).width = width
                        col += 1
                    # 详细信息
                    elif type(aa) == list:
                        for a in aa:
                            sheet.write(row, col, a, self.style1)
                            data_length_index = len(a.encode('utf-8'))  # 获取当前Unicode字符串长度
                            if data_length_index > 10:
                                width = int(256 * (data_length_index + 1) * 1.3)
                                if width > 65535:
                                    sheet.col(row).width = 65535
                                else:
                                    sheet.col(row).width = width
                            col += 1
                        if aa != index[-1]:
                            row += 1
                        else:
                            pass
                        col = 0
            total += 1
            row += 1
            print(index)
        # 保存表格
        try:
            new.save(self.create_name)
            print('保存表格成功，当前时间为： ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except PermissionError:
            print('文件未关闭，保存失败，请关闭文件后重试')
            pass


if __name__ == '__main__':
    excel = Excel()
    excel.excel_create(content_title=index_name, content=index_list)
