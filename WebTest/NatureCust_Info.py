# -*- coding: utf-8 -*-
import re
import traceback
import requests
import json
import xlrd


# Excel读取/创建文件
class Excel:
    def __init__(self, file='./output_file/Code_data.xls', colindex=0, by_index=0):
        self.file = file
        self.colindex = colindex
        self.by_index = by_index

    def open_excel(self):  # 打开要解析的Excel文件
        try:
            data = xlrd.open_workbook(self.file)
            return data
        except Exception as e:
            print(e)

    def testcase_index(self):  # 读取组织机构信息
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
        tab = data.sheets()[self.by_index + 0]  # 选择excel里面的Sheet
        col_name = tab.row_values(self.colindex)
        list_results = []  # 创建一个空列表
        app = {}  # 创建空字典
        for num, name in enumerate(col_name):  # 第一行为标题（第一行为0），所以从第二行开始
            app[name] = ''
        list_results.append(app)
        return list_results


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


if __name__ == '__main__':
    excel = Excel()
    print(excel.testcase_index())
    nautureinfo_get()
