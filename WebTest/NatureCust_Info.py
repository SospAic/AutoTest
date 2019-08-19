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


def excel_by_index(file='./output_file/Code_data.xls', by_index=0):  # 按表的索引读取
    """通过抓取的统一社会信用代码证创建"""
    data = open_excel(file)  # 打开excel文件
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
def nautureinfo_get(vendor_name='', org_code='601071541'):
    url_add = 'http://10.124.150.230:8000/api/jzjk/NatureCustIntfSerApi/qryEnterpriseInfo/v0'
    s = requests.session()
    try:
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'Accept-Encoding': '',
        }
        request_data = json.dumps(
            {
                "UNI_BSS_ATTACHED": {
                    "MEDIA_INFO": "he5xpipkepn4t3M17wABiKesd2od7ayiDMpOfKCcqJxboowBaxk2kwkNgyBCIabuoOaElvnzKemGqL90mG07lepq6FOAGhqlsJwFGhwA6IIANpbeLFqIKKrMx8fmpd3JHFAD7F0MyJxEvMpwdCott6fPiL1i4iLG415wa2wOpDgE8isq8Hpe1d4qBCHbPOCF1nav7wwzJ0azL20Hve8jHzzCidA5f7wNJp13pE7eMqhJclMEgM4MNdDm9rejf8Efjc2O8cCE7pLJs25ItJyBHea7u1JL7enrlsHD5i51nbuNGFL8EMbHE2uAlrvMcHEgdwt5H6DkC2Iw3iBnnL08MeH2xtJC9FsOE1hGuKNl9PM2aewO74ftkJPcwKkt3Pv66vaFHkP6463nPvw0wsyanH3rcoP1xupMbukOhwAcLrHrv48q6rks1EmmPBO6H1JHvKnxhM9FGxpqdaprdk69r"
                },
                "UNI_BSS_BODY": {
                    "REQ": {
                        "VENDOR_NAME": vendor_name,
                        "ORG_CODE": org_code,
                        "USER_CODE": "test",
                        "DOMAIN": "B",
                        "SOURE_SYSTEM_NAME": "",
                        "EPARCHY_CODE": "0kiO",
                        "USER_NAME": "测试_杜",
                        "PROVINCE_CODE": "10",
                        "SEARCH_FLAG": "0",
                        "SOURE_SYSTEM_ID": "HJ-BBSS"

                    }
                },
                "UNI_BSS_HEAD": {
                    "APP_ID": "5UPmcd0ARr",
                    "TIMESTAMP": "2019-07-15 18:56:25 055",
                    "TRANS_ID": "20190715185625055160667",
                    "TOKEN": "4deb4fc0629e154659586d15f4f4fd43"
                }
            }
        )
        print(json.dumps(request_data))
        rs = s.post(url_add, headers=headers, data=request_data, timeout=5)
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
        nautureinfo_get(nature_info[0], nature_info[1])
        time.sleep(1)
    print('处理完成')


if __name__ == '__main__':
    sys.stdout = Logger('./log/政企自然客户查询.log')
    get_info()
