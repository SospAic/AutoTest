import os
import random
import time
import pytesseract
import xlrd
import xlwt
from aip import AipOcr
from selenium import webdriver
from PIL import Image, ImageEnhance
from WebTest.Selenium_driver_base import selenium_driver
from xlutils3.copy import copy


class BaiduAip:

    def __init__(self):
        # API
        self.APP_ID = '24107714'
        self.API_KEY = 'guKhh1ICHk3oFjoxWQZS8jIS'
        self.SECRET_KEY = 'cAvRRxhIO19dONgQSfftTDyRsSOR7N5t'
        # 初始化AipFace对象
        self.client = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        # 可选参数
        self.options = {}
        self.options["language_type"] = "CHN_ENG"  # 中英文混合
        self.options["detect_direction"] = "true"  # 检测朝向
        self.options["detect_language"] = "true"  # 是否检测语言
        self.options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    def get_file_content(self, filepath):
        """ 读取图片 """
        with open(filepath, 'rb') as fp:
            return fp.read()

    def img_to_str(self, image_path):
        """带参数调用通用文字识别"""
        self.get_file_content(image_path)
        result = self.client.basicGeneral(self.get_file_content(filePath), self.options)
        # 格式化输出-提取需要的部分
        if 'words_result' in result:
            text = ('\n'.join([w['words'] for w in result['words_result']]))
        print(type(result), "和", type(text))
        print(result, text)
        # """ save """
        # fs = open("baidu_ocr.txt", 'w+')  # 将str,保存到txt
        # fs.write(text)
        # fs.close()
        return text


class Excel:
    def __init__(self, filename='./output_file/define_info_data.xls'):
        """ 设置表头单元格及文本样式 """
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
        # 列名
        self.table_top_list = ['企业名称', '统一社会信用代码', '注册资本', '工商注册号', '组织机构代码', '注册地址', '行业']
        self.filename = filename

    def excel_create(self, file_path):
        """ 创建表格 """
        # create_num = str(random.randint(1, 1000))
        # create_date = time.strftime('%Y%m%d', time.localtime(time.time())) # 创建日期，可配合随机码使用
        if os.path.exists(self.filename):
            # 打开已有表
            old = xlrd.open_workbook(self.filename, formatting_info=True)
            # 复制原有表
            new = copy(old)
        else:
            # 创建文件
            new = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建Sheet页
        sheet = new.add_sheet(key_value, cell_overwrite_ok=True)
        # 写入表头
        print('开始创建表格')
        for row in range(len(self.table_top_list)):
            write_data = self.table_top_list[row]
            sheet.write(0, row, write_data, self.style)
            data_length_index = len(write_data.encode('utf-8'))  # 获取当前Unicode字符串长度
            """设置单元格宽度"""
            if data_length_index > 10:
                sheet.col(row).width = 256 * (data_length_index + 1)
            print('列名共{0:>2}条,正在添加：{1}'.format(str(len(self.table_top_list)), write_data))
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


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=selenium_driver())  # Chrome配置参数
    filePath = './pic_code/vcode.jpg'
    baidu_ocr = BaiduAip()
    print(baidu_ocr.img_to_str(filePath))
    print("识别完成。")
