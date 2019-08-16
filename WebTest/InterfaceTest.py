import os
import random
import sys
import time
import urllib.request
import json
import pymysql
import requests
import xlrd
import re
import time
import xlwt
import traceback
from PIL import Image
from xlutils3.copy import copy


# 数据库操作
class MySQL:
    def __init__(self, host=None, name=None, pwd=None, schema=None):
        self.host = host
        self.name = name
        self.pwd = pwd
        self.schema = schema
        self.db = pymysql.connect(self.host, self.name, self.pwd, self.schema)
        self.cursor = self.db.cursor()

    def sql_execute(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取字段名
            index = self.cursor.description
            # 获取所有记录列表
            results = self.cursor.fetchall()
            execute_results = []
            for row in results:
                execute_add = []
                for c in range(0, len(index)):
                    data = str(index[c][0]) + ' = ' + str(row[c])
                    execute_add.append(data)
                    # print(data)
                execute_results.append(execute_add)
            # print(execute_results)  # 输出查询结果
            return execute_results
        except:
            print('未查询到指定数据，请检查SQL语句，错误详情：')
            traceback.print_exc()
            pass
        # self.db.close()  # 关闭数据库连接

    # 获取字段信息
    def database_description(self, table_name, schema=None):
        try:
            self.cursor.execute("SELECT t.column_name '字段名',"
                                "t.COLUMN_TYPE '数据类型',"
                                "t.IS_NULLABLE '可为空',"
                                "t.COLUMN_KEY '主键',"
                                "t.COLUMN_DEFAULT '默认值',"
                                "t.COLUMN_COMMENT '注释'"
                                " FROM information_schema.COLUMNS t WHERE table_schema = '{}'"
                                " AND table_name = '{}'".format(schema, table_name))
            # 获取字段名
            index = self.cursor.description
            # 获取所有记录列表
            results = self.cursor.fetchall()
            column_information = []
            for row in results:
                column_add = {}
                for c in range(0, len(index)):
                    column_add[index[c][0]] = row[c]
                    # print(index[c][0], row[c])
                column_information.append(column_add)
            # print(column_information)  # 展示所有信息
            # self.db.close()  # 关闭数据库连接
            return column_information
        except:
            print('未查询到字段信息，请检查SQL语句，错误详情：')
            traceback.print_exc()
            pass


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


# Dump/Load Cookie
def get_cookie(file='./input_file/cookie.txt'):
    f2 = open(file)
    cookie = f2.read()
    cookie = json.loads(cookie)
    cookies = []
    for c in cookie:
        cookies.append(c)
    return cookies


# Str to Json
def str_to_dict(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    return cookies


# Get/Post 请求
def request_get(url_add, method='post', request_data=None):
    try:
        # 调试模式，范文
        headers = {
            'POST /cust-web/cust/CustInfoController/qryCustInfoList.do HTTP/1.1'
            'Host': '10.124.146.175',
            'Connection': 'keep-alive',
            'Content-Length': '100',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://10.124.146.175',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.5.4000',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Cookie': 'PORTALSESSION=aaa6e888-6712-4a2d-8c1e-f095844ed70f; '
                      'SERVERID=34763c1f1acb34871d8360c4c56f649a|1554472970|1554472964',
            'Referer': 'http://10.124.146.175/cust-web/custIndex.html?viewName=CustInfoDataView&portalSessionId=e79a2d58'
                       '-96e9-436f-a3a3-6179e41fde5c&acquireUrl=http://10.124.156.55/portal-web/portal/SessionController'
                       '/qryLoginInfo.do',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN',
        }
        # 简化模式，初次登录须校验，添加反爬
        headers1 = {"Content-Type": "application/json;charset=UTF-8",
                    "Referer": url_add}
        if method == 'get':
            rs = s.get(url_add, params=request_data, timeout=5)  # 加入超时限制
            # print(rs.text)
        else:
            # rs = s.post(url_add, headers=headers, data=request_data, timeout=5)  # 加入超时限制
            cookies = s.cookies.get_dict()
            rs = s.post(url_add, headers=headers1, data=request_data, cookies=cookies, timeout=5)
            # print(rs.text)
        print('返回状态码：{}'.format(rs.status_code))
        return rs
    except requests.exceptions.ConnectTimeout:
        print('连接超时，错误详情：')
        traceback.print_exc()
        pass
    except requests.exceptions.ReadTimeout:
        print('读取超时，请检查网络，错误详情：')
        traceback.print_exc()
        pass
    except requests.exceptions.ConnectionError:
        print('连接拒绝，请检查网络，错误详情：')
        traceback.print_exc()
        pass


# Login登录校验(Session)
def login_check(url):
    # Session定义在入口函数里，方便调用
    urllib.request.urlretrieve('http://10.124.156.55/portal-web/portal/LoginController/vcode.do?1554363712307',
                               './out_img/interface.jpg')
    im = Image.open('./out_img/interface.jpg')
    im.show()
    code = input('请输入验证码：')
    loginUrl = url
    postData = {"userCode": "admin", "password": "gkgldadacnfagbhdhdhhgphcge", "verifyCode": code, "clientType": "1000",
                "browserType": "Chrome", "loginWay": "password"}
    rs = s.post(loginUrl, data=postData, timeout=5)
    # print(rs.status_code)
    return rs


# Excel读取/创建文件
class Excel:
    def __init__(self, file='./input_file/接口用例.xls', colindex=0, by_index=0):
        self.file = file
        self.colindex = colindex
        self.by_index = by_index

    def open_excel(self):  # 打开要解析的Excel文件
        try:
            data = xlrd.open_workbook(self.file)
            return data
        except Exception as e:
            print(e)

    def testcase_index(self):  # 读取用例内容
        data = self.open_excel()  # 打开excel文件
        tab = data.sheets()[self.by_index]  # 选择excel里面的Sheet
        n_rows = tab.nrows  # 行数
        n_cols = tab.ncols  # 列数
        col_name = tab.row_values(self.colindex)  # 第0行的值
        list_create = []  # 创建一个空列表
        for x in range(1, n_rows):  # 第一行为标题（第一行为0），所以从第二行开始
            row = tab.row_values(x)
            # if row[-1] == '是':
            if re.search('是', row[-1], re.I):
                app = {}  # 创建空字典
                for y in range(0, n_cols):
                    app[col_name[y]] = row[y]
                list_create.append(app)
            else:
                continue
        return list_create

    def result_index(self):  # 读取标题内容
        data = self.open_excel()  # 打开excel文件
        tab = data.sheets()[self.by_index + 1]  # 选择excel里面的Sheet
        col_name = tab.row_values(self.colindex)
        list_results = []  # 创建一个空列表
        app = {}  # 创建空字典
        for num, name in enumerate(col_name):  # 第一行为标题（第一行为0），所以从第二行开始
            app[name] = ''
        list_results.append(app)
        return list_results

    # 创建表格
    def excel_create(self, file_path='./input_file/接口用例.xls'):
        if os.path.exists('./input_file/接口用例.xls'):
            # 打开已有表
            old = xlrd.open_workbook('./input_file/接口用例.xls', formatting_info=True)
            # 复制原有表
            new = copy(old)
        else:
            # 创建文件
            new = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 创建Sheet页
        try:
            sheet = new.add_sheet('测试结果', cell_overwrite_ok=True)
        except:
            sheet = new.get_sheet('测试结果')
        # 设置表头单元格及文本样式
        # 通过样式
        style = xlwt.easyxf(
            "font: bold False, colour white, name 微软雅黑;"
            "pattern: pattern solid, fore_colour green;"
            "alignment: horizontal center,vertical center;"
            "borders: left 1, right 1, top 1, bottom 1, "
            "left_colour black, right_colour black, top_colour black, bottom_colour black;"
        )
        # 未通过样式
        style1 = xlwt.easyxf(
            "font: bold False, colour black, name 微软雅黑;"
            "pattern: pattern solid, fore_colour red;"
            "alignment: horizontal center,vertical center;"
            "borders: left 1, right 1, top 1, bottom 1, "
            "left_colour black, right_colour black, top_colour black, bottom_colour black;"
        )
        # 标题样式
        style2 = xlwt.easyxf(
            "font: bold True, colour white, name 微软雅黑;"
            "pattern: pattern solid, fore_colour light_blue;"
            "alignment: horizontal center,vertical center;"
            "borders: left 2, right 2, top 2, bottom 2, "
            "left_colour black, right_colour black, top_colour black, bottom_colour black;"
        )
        # 写入表头
        test_results = list(excel.result_index()[0])
        for row in range(len(test_results)):
            write_data = test_results[row]
            sheet.write(0, row, write_data, style2)
        # 写入内容
        print('开始写入数据')
        for col in range(len(run_results)):
            write_data = list(run_results[col].values())
            print('共计{0:>3}条用例，当前为{1:>3}条，用例名称为：{2}'.format(len(run_results), col + 1, write_data[1]))
            for row in range(len(run_results[col])):
                if write_data[-2] == '未通过':  # 当调整表格字段时注意此处设置
                    sheet.write(col + 1, row, write_data[row], style1)
                else:
                    sheet.write(col + 1, row, write_data[row], style)
                data_length_index = len(str(write_data[row]).encode('utf-8'))  # 获取当前Unicode字符串长度
                if row == 2 or row == 3:  # 请求和返回值过长，设固定值
                    sheet.col(row).width = 6000
                elif row == 13:
                    sheet.col(row).width = 15000
                else:
                    if data_length_index > 10:
                        width = int(256 * (data_length_index + 1) * 1.3)
                        if width > 65535:
                            sheet.col(row).width = 65535
                        else:
                            sheet.col(row).width = width
        # 保存表格
        try:
            new.save(file_path)
            print('保存表格成功，当前时间为： ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except PermissionError:
            print('文件未关闭，保存失败，请关闭文件后重试')
            pass


# 执行用例
def run_test(url, method, param, expect=None, sql_server=None, sql_account=None, sql_pwd=None, sql_schema=None,
             sql_execute=None, contrast=None, limit=None, num=None):
    try:  # 首先判断不带数据库的接口入参
        req = request_get(url_add=url, method=method, request_data=param)
        test_result = excel.result_index()[0].copy()  # 测试结果表头
        case_index = excel.testcase_index()[num - 1].copy()  # 用例测试结果Dict-Key
        # 字段对应
        test_result['编号'] = case_index['编号']
        test_result['用例名称'] = case_index['用例名称']
        test_result['请求报文'] = str(req.headers)
        test_result['返回报文'] = str(req.text)
        test_result['对比参数'] = case_index['对比参数']
        test_result['字段预期属性'] = case_index['字段预期属性']
        test_result['预期返回值'] = expect
        test_result['返回码'] = req.status_code
        test_result['说明'] = ' '
        test_result['是否通过'] = '未通过'
        try:  # 预期返回值判断
            pass_check = test_result['预期返回值'].split('=')
            pass_code = '"{}":"{}"'.format(pass_check[0], pass_check[1])
            search = re.search(pass_code, req.text, re.I)
            if search is not None:
                test_result['实际返回值'] = pass_code
                test_result['是否通过'] = '通过'
                test_result['说明'] = '状态码+request校验'.strip()
            else:
                text = r'"{}":"'.format(pass_check[0])
                show_text = re.search(r'{}(\d)"'.format(text), req.text, re.I)
                test_result['实际返回值'] = show_text.group(0)
                test_result['是否通过'] = '未通过'
                test_result['说明'] = '状态码+request校验'
        except IndexError:
            print('预期返回值为空?请检查')
            test_result['预期返回值'] = '空'
            test_result['实际返回值'] = '空'
            test_result['说明'] = '状态码+request校验'
            pass
        except AttributeError:
            print('预期返回值为空?请检查')
            test_result['预期返回值'] = '空'
            test_result['实际返回值'] = '空'
            test_result['说明'] = '状态码+request校验'
            pass
        # 判断含有数据库信息的接口入参
        if sql_server and sql_account and sql_pwd and sql_schema and sql_execute is not None:
            mysql = MySQL(sql_server, sql_account, sql_pwd, sql_schema)
            mysql.sql_execute(sql_execute)
            table_name = re.search('from (.*) where', sql_execute, re.I)
            description = mysql.database_description(table_name.group(1), sql_schema)  # 调用数据库各字段参数
            try:  # 切割字段类型及长度
                limit_keywords = str(limit).split('|')
                limit_check = limit_keywords[1].split('=')
                for check_name in description:
                    if check_name['字段名'] == limit_keywords[0]:
                        check_data = re.search('{}(.*)'.format(limit_check[0]), check_name['数据类型'], re.I)  # 正则查询值
                        if check_data is not None:
                            check_keyword = check_data.group(1).strip()[1:-1]
                            if check_keyword == limit_check[1]:
                                print('数据类型正确，限定："{}"，实际："{}"'.format(limit_keywords[1], check_name['数据类型']))
                                test_result['字段实际属性'] = check_name['数据类型']
                                test_result['字段预期属性'] = limit_keywords[1]
                                test_result['校验结果'] = '通过'
                                test_result['说明'] = '{},数据库字段校验'.format(test_result['说明'])
                                break
                            else:
                                print('数据类型错误，限定：{}，实际：{}({})'.format(limit_keywords[1], limit_check[0], check_keyword))
                                test_result['字段实际属性'] = check_name['数据类型']
                                test_result['字段预期属性'] = limit_keywords[1]
                                test_result['校验结果'] = '未通过'
                                test_result['说明'] = '{},数据库字段校验'.format(test_result['说明'])
                                if test_result['是否通过'] == '通过':
                                    test_result['是否通过'] = '未通过'
                                break
                        else:
                            print('未找到符合条件的字段，请检查用例参数')
                            test_result['字段实际属性'] = check_name['数据类型']
                            test_result['字段预期属性'] = limit_keywords[1]
                            test_result['校验结果'] = '未通过'
                            test_result['说明'] = '{},数据库字段校验'.format(test_result['说明'])
                            if test_result['是否通过'] == '通过':
                                test_result['是否通过'] = '未通过'
            except IndexError:
                print('字段预期属性为空?请检查')
                test_result['字段预期属性'] = '无'
                test_result['校验结果'] = '无'
                pass
        else:
            print('无数据库信息，跳过')
            test_result['校验结果'] = '无'
            test_result['字段实际属性'] = '无'
            test_result['字段预期属性'] = '无'
        if contrast is not None:  # 对比入参
            try:
                constract_name = contrast.split('=')
                contrast_title = constract_name[0].replace('_', '')
                contrast_check = re.search('"{}":"{}"'.format(contrast_title, constract_name[1]), req.text, re.I)
                if contrast_check is not None:
                    print('对比结果正确，限定："{}"，实际："{}"'.format(contrast, contrast_check.group(0)))
                    test_result['对比结果'] = '通过'
                    test_result['说明'] = '{},返回值对比数据库校验'.format(test_result['说明'])
                else:
                    contrast_error = re.search('"{}":(.*?),'.format(contrast_title), req.text, re.I)
                    print('对比结果错误，限定："{}"，实际：{}'.format(contrast, contrast_error.group(1)))
                    test_result['对比结果'] = '未通过'
                    test_result['说明'] = '{},返回值对比数据库校验'.format(test_result['说明'])
                    if test_result['是否通过'] == '通过':
                        test_result['是否通过'] = '未通过'
            except IndexError:
                print('字段限制无法校验，跳过')
                test_result['对比结果'] = '无'
                pass
            except AttributeError:
                print('字段限制无匹配结果，跳过')
                test_result['对比结果'] = '无'
                pass
        else:
            print('无对比参数，跳过')
            test_result['对比参数'] = '空'
            test_result['对比结果'] = '空'
            pass
        # print(test_result)
        run_results.append(test_result)
    except TypeError:
        traceback.print_exc()
    except AttributeError:
        traceback.print_exc()
    return run_results


# 用例列表
def testcase_list():
    start = time.time()  # time.process_time()
    testcase_total = excel.testcase_index()
    a = 1
    for testcase in testcase_total:
        print('{0}\n正在执行第{1:>3}条：{2}用例'.format(('*' * 100), int(testcase['编号']), testcase['用例名称']))
        run_test(num=a, url=testcase['请求地址'], method=testcase['请求方式'],
                 param=testcase['请求参数'], expect=testcase['预期返回值'], sql_server=testcase['数据库地址'],
                 sql_account=testcase['数据库账号'], sql_pwd=testcase['数据库密码'], sql_schema=testcase['数据库名称'],
                 sql_execute=testcase['执行语句'], contrast=testcase['对比参数'], limit=testcase['字段预期属性'])
        a += 1
    end = time.time()  # time.process_time()
    print('执行完成，共计{}条用例，用时{}秒'.format(len(testcase_total), (end - start)))
    excel.excel_create()
    return 1


if __name__ == '__main__':
    sys.stdout = Logger('./log/接口测试日志.log')
    s = requests.session()
    excel = Excel()
    run_results = []
    # login_check('http://10.124.156.55/portal-web/index.jsp')  # 测试环境校验
    # login_check('http://10.124.166.82/portal-web/index.jsp') # 准生产环境校验
    # login_check('http://10.124.166.77/portal-web/index.jsp') # 生产环境校验
    testcase_list()
