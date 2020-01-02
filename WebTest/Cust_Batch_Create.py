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


# 发送认证
def nature_info_get(num, before_num, cust_name='测试客户', org_code='HLJ15010', release_date='1224'):
    url_add = 'http://10.124.146.175/cust-web/cust/CustInfoController/createCustInfo.do'
    s = requests.session()
    for create_num in range(before_num + 1, num + before_num + 1):
        try:
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/json',
                'Accept-Encoding': '',
                'Cookie': 'PORTALSESSION=6a4e29a8-9a9c-45d0-855a-a0aa60be54f7; '
                          'SERVERID=34763c1f1acb34871d8360c4c56f649a|1577088620|1577088564'
            }
            request_data = json.dumps(
                {
                    "operType": "Add",
                    "custInfo": {
                        "custName": "{0}{1}{2:03d}".format(cust_name, release_date, create_num),
                        "inMethod": "G",
                        "isPassOrg": "0",
                        "custClassType": "2",
                        "tempProvinceCode": "哈尔滨-哈尔滨市区",
                        "postAddr": "这是一条测试地址",
                        "postCode": "150000",
                        "contactName": "张小三",
                        "contactPhone": "1366666666",
                        "callingTypeCode": "公共服务业-基础服务业-电力的生产和供应",
                        "callingTypeCodeValue": "06,0601,060101",
                        "groupMemo": "",
                        "dataState": "J",
                        "isImp": "0",
                        "provinceCode": "97",
                        "eparchyCode": "971",
                        "bcityCode": "974214",
                        "firstCallingTypeCode": "06",
                        "secondCallingTypeCode": "0601",
                        "thirdCallingTypeCode": "060101"
                    },
                    "custTransactor": {
                        "transactorName": "吴余额",
                        "certiTypeCode": "1",
                        "certiCode": "371523199206055312",
                        "isReal": "1",
                        "phone": "136666666",
                        "certiAddr": "这是一条测试地址"
                    },
                    "custManagerRels": [],
                    "custCreditCerti": {
                        "certCode": "{0}{1}000{2:03d}".format(org_code, release_date, create_num),
                        "certName": "{0}{1}{2:03d}".format(cust_name, release_date, create_num),
                        "addr": "这是一条测试地址",
                        "legalName": "张小三",
                        "certFileName": "cus_统一社会信用代码证_20191213091439.jpg",
                        "certFileid": "210694",
                        "mainCertFlag": "1"
                    },
                    "files": [],
                    "custContacts": [],
                    "custEvents": [],
                    "asys": []
                }
            )
            request_data1 = json.dumps(
                {
                    "operType": "Add",
                    "custInfo": {
                        "custName": "{0}{1}{2:03d}".format(cust_name, release_date, create_num),
                        "inMethod": "G",
                        "isPassOrg": "0",
                        "custClassType": "2",
                        "tempProvinceCode": "重庆市-万州区",
                        "servLevelId": "0",
                        "postAddr": "这是一条测试地址",
                        "postCode": "404100",
                        "contactName": "张小三",
                        "contactPhone": "1366666666",
                        "contactEmail": "abc@123.com",
                        "vocaDeptTypeId": "3",
                        "callingTypeCode": "科学、教育、文化体育、卫生、出版业-广播电影电视业-广播",
                        "callingTypeCodeValue": "03,0305,030501",
                        "officeType": "2",
                        "groupMemo": "",
                        "dataState": "J",
                        "isImp": "0",
                        "provinceCode": "83",
                        "eparchyCode": "831",
                        "bcityCode": "832001",
                        "firstCallingTypeCode": "03",
                        "secondCallingTypeCode": "0305",
                        "thirdCallingTypeCode": "030501"
                    },
                    "custTransactor": {
                        "transactorName": "吴余额",
                        "certiTypeCode": "1",
                        "certiCode": "371523199206055312",
                        "isReal": "1",
                        "phone": "1366666666",
                        "certiAddr": "这是一条测试地址"
                    },
                    "custManagerRels": [],
                    "custCreditCerti": {
                        "certCode": "{0}{1}000{2:03d}".format(org_code, release_date, create_num),
                        "certName": "{0}{1}{2:03d}".format(cust_name, release_date, create_num),
                        "addr": "这是一条测试地址",
                        "legalName": "张小三",
                        "certFileName": "cus_统一社会信用代码证_20191220101233.jpg",
                        "certFileid": "212050",
                        "mainCertFlag": "1"
                    },
                    "files": [],
                    "custContacts": [],
                    "custEvents": [],
                    "asys": []
                }
            )
            # print(json.dumps(request_data))
            rs = s.post(url_add, headers=headers, data=request_data)
            print(rs.text)
            print('返回状态码：{}'.format(rs.status_code))
            time.sleep(2)
        except requests.exceptions.ConnectTimeout:
            print('连接超时，错误详情：')
            traceback.print_exc()
            pass
    print('创建完成')


if __name__ == '__main__':
    sys.stdout = Logger('./log/实体客户批量创建.log')
    patch_num = input('请输入创建客户数量：')
    patch_num = int(patch_num)
    before_num = input('请输入跳过编码数量：')
    before_num = int(before_num)
    print('共计{0:>2}条数据'.format(patch_num))
    nature_info_get(patch_num, before_num)
