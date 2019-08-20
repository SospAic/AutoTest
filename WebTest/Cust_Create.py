# -*- coding: utf-8 -*-
import sys
import time
import traceback
import requests
import json
import xlrd


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


def open_excel(file='./output_file/Code_data.xls'):  # 打开要解析的Excel文件
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(e)


def excel_by_index(file='./output_file/Code_data.xls', by_index=0, timeout=5):  # 按表的索引读取
    """通过抓取的统一社会信用代码证创建"""
    data = open_excel(file)  # 打开excel文件
    # start_time = time.time()
    select_num = input('{}\n请输入查询的Sheet页号（1到{}）：'.format(data.sheet_names(), len(data.sheet_names())))
    select_num = int(select_num)
    if 0 < select_num <= len(data.sheet_names()):
        by_index = select_num - 1
        print('当前选择页为：{}'.format(data.sheet_names()[by_index]))
    else:
        by_index = 0
        print('输入的页码有误，默认取第一页，输出页为：{}'.format(data.sheet_names()[by_index]))
    tab = data.sheets()[by_index]  # 选择excel里面的Sheet
    n_rows = tab.nrows  # 行数
    list_create = []  # 创建一个空列表
    for x in range(1, n_rows):  # 第一行为标题（第一行为0），所以从第二行开始
        row = tab.row_values(x, start_colx=0, end_colx=2)
        if row[0] is '-' or None:  # 判断空白或占位符
            continue
        else:
            list_create.append(row)
    return list_create


# 发送认证
def nature_info_get(cust_name='', org_code='601071541'):
    url_add = 'http://10.124.146.175/cust-web/cust/CustInfoController/createCustInfo.do'
    s = requests.session()
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'Accept-Encoding': '',
            'Cookie': 'PORTALSESSION=4e86818f-d6a2-4c72-8e6a-654d664c6119; '
                      'SERVERID=34763c1f1acb34871d8360c4c56f649a|1566199204|1566198940'
        }
        request_data = json.dumps(
            {
                "operType": "Add",
                "custInfo": {
                    "custName": cust_name,
                    "inMethod": "G",
                    "orgCode": org_code,
                    "orgCode2": "",
                    "isPassOrg": "1",
                    "custClassType": "2",
                    "tempProvinceCode": "内蒙古-锡林郭勒盟-二连浩特市",
                    "postAddr": "北京市海淀区上地信息路3号",
                    "postCode": "126001",
                    "contactName": "张小三",
                    "contactPhone": "136666666666",
                    "callingTypeCode": "采掘业和加工、制造业-采矿业-石油和天然气开采业",
                    "callingTypeCodeValue": "05,0501,050101",
                    "provinceCallingType": "采掘业和加工、制造业-电气机械及器材制造业-制造",
                    "provinceCallingTypeValue": "9,930,93002",
                    "groupMemo": "",
                    "dataState": "J",
                    "isImp": "0",
                    "provinceCode": "10",
                    "eparchyCode": "111",
                    "bcityCode": "102087",
                    "firstProvinceCallingType": "9",
                    "secondProvinceCallingType": "930",
                    "thirdProvinceCallingType": "93002",
                    "firstCallingTypeCode": "05",
                    "secondCallingTypeCode": "0501",
                    "thirdCallingTypeCode": "050101"
                },
                "custTransactor": {
                    "transactorName": "吴延华",
                    "certiTypeCode": "1",
                    "certiCode": "371523199206055312",
                    "isReal": "1",
                    "certiAddr": "这是一条测试地址",
                    "phone": "13666666666"
                },
                "custManagerRels": [],
                "custBusiLicense": {
                    "licenseType": "3",
                    "certName": cust_name,
                    "certCode": org_code,
                    "addr": "北京市海淀区上地信息路3号",
                    "legalName": "孙亚芳",
                    "busiArea": "从事通信产品的研发、销售及技术服务;货物进出口、代理进出口、技术进出口。(依法须经批准的项目,经相关部门批准后依批准的内容开展经营活动。)",
                    "sendDate": "2016-06-30",
                    "isCreditCode": "1",
                    "certFileName": "cus_营业执照_20190819151952.jpg",
                    "certFileid": "45302",
                    "mainCertFlag": "1"
                },
                "files": [],
                "custContacts": [],
                "custEvents": [],
                "asys": []
            }
        )
        print(json.dumps(request_data))
        rs = s.post(url_add, headers=headers, data=request_data)
        print(rs.text)
        print('返回状态码：{}'.format(rs.status_code))
        return rs
    except requests.exceptions.ConnectTimeout:
        print('连接超时，错误详情：')
        traceback.print_exc()
        pass


def get_info():
    nature_list = excel_by_index()[:]
    print('共计{0:>2}条数据'.format(len(nature_list)))
    for nature_info in nature_list:
        print('当前组织名称：{}，统一社会信用代码：{}'.format(nature_info[0], nature_info[1]))
        nature_info_get(nature_info[0], nature_info[1])
        time.sleep(1)
    print('处理完成')


if __name__ == '__main__':
    sys.stdout = Logger('./log/实体客户创建.log')
    get_info()
