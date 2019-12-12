# -*- coding: utf-8 -*-
import sys
import traceback
import requests
import json


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


# 模拟报文创建
def taxpayer_get(create_num=1):
    url_add = 'http://10.124.146.175/cust-web/cust/TaxpayerInfoController/createTaxpayerInfo.do'
    s = requests.session()
    for num in range(create_num):
        try:
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/json',
                'Accept-Encoding': '',
                'Cookie': ''
            }
            request_data = json.dumps(
                {
                    "taxpayerId": "",
                    "taxpayerCode": "HLJ150101121000{0:03d}".format(num),
                    "taxpayerName": "测试客户1121{0:03d}".format(num),
                    "orgCode": "",
                    "socialCode": "",
                    "address": "这是一条测试地址",
                    "cellNumber": "1366666666",
                    "bankName": "测试银行",
                    "bankAccount": "123456789001",
                    "isComTaxpayer": "1"
                }
            )
            print(json.dumps(request_data))
            rs = s.post(url_add, headers=headers, data=request_data)
            print(rs.text)
            print('返回状态码：{}'.format(rs.status_code))
        except requests.exceptions.ConnectTimeout:
            print('连接超时，错误详情：')
            traceback.print_exc()
            pass


if __name__ == '__main__':
    sys.stdout = Logger('./log/纳税人资质创建.log')
    taxpayer_get(20)
