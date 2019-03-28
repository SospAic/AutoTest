import random
import requests

# -*- coding: utf-8 -*-
# 统一社会信用代码中不使用I,O,Z,S,V
SOCIAL_CREDIT_CHECK_CODE_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
    'P': 23, 'Q': 24,
    'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}
# GB11714-1997全国组织机构代码编制规则中代码字符集
ORGANIZATION_CHECK_CODE_DICT = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22,
    'N': 23, 'O': 24, 'P': 25, 'Q': 26,
    'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}


class CreditIdentifier(object):
    """通过前15位生成统一社会信用代码"""

    def CreateC9(self, code):
        # 第i位置上的加权因子
        weighting_factor = [3, 7, 9, 10, 5, 8, 4, 2]
        # 第9~17位为主体标识码(组织机构代码)
        organization_code = code[8:17]
        # 本体代码
        ontology_code = organization_code[0:8]
        # 生成校验码
        tmp_check_code = self.gen_check_code(
            weighting_factor, ontology_code, 11, ORGANIZATION_CHECK_CODE_DICT)
        return code[:16] + tmp_check_code

    def getSocialCreditCode(self, code):
        code = self.CreateC9(code[:16])
        # 第i位置上的加权因子
        weighting_factor = [1, 3, 9, 27, 19, 26, 16,
                            17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
        # 本体代码
        ontology_code = code[0:17]
        # 计算校验码
        tmp_check_code = self.gen_check_code(
            weighting_factor, ontology_code, 31, SOCIAL_CREDIT_CHECK_CODE_DICT)
        return code[:17] + tmp_check_code

    def gen_check_code(self, weighting_factor, ontology_code, modulus, check_code_dict):
        total = 0
        for i in range(len(ontology_code)):
            if ontology_code[i].isdigit():
                total += int(ontology_code[i]) * weighting_factor[i]
            else:
                total += check_code_dict[ontology_code[i]
                         ] * weighting_factor[i]
        C9 = modulus - total % modulus
        C9 = 0 if C9 == 31 else C9
        C9 = list(check_code_dict.keys())[
            list(check_code_dict.values()).index(C9)]
        return C9


def code_read(filename='Code_list.txt'):
    """加载组织机构代码"""
    f = open(filename)
    code_list = []
    for line in f.readlines():
        curLine = line.strip().split()
        code_list.append(curLine)
    return code_list


class Counter:
    """计数器"""

    def __init__(self, start=0):
        self.num = start

    def count(self):
        self.num += 1
        return self.num


def OrgCode():
    """组织机构代码证随机生成"""
    factor_list = [3, 7, 9, 10, 5, 8, 4, 2]  # 加权因子列表
    org_code = []  # 用于存放生成的组织机构代码
    sum_1 = 0
    for i in range(8):  # 随机取前8位数字
        org_code.append(random.randint(1, 9))  # 随机取1位数字
        sum_1 = sum_1 + org_code[i] * factor_list[i]  # 用orgCode*加权因子
        # print(dd)
    for i in range(len(org_code)):
        org_code[i] = str(org_code[i])  # 将orgCode（int）变成str
    c9 = 11 - sum_1 % 11  # C9代表校验码。用已经生成的前8位加权后与11取余，然后用11减
    # print(c9)
    if c9 == 10:  # 当C9的值为10时，校验码应用大写的拉丁字母X表示；当C9的值为11时校验码用0表示;除此之外就是C9本身
        c9 = 'X'
    else:
        if c9 == 11:
            c9 = '0'
        else:
            c9 = str(c9)
    org_code.append('-' + c9)
    return "".join(org_code)  # 拼接最终生成的组织代码


def post_check(url):
    params = {"access_token": "b3c40922-8c96-401f-ac3f-b49bd7dabfd9"}
    payload = {
        "filterVal": "",
        "anyProperties": {"provinceCode": "97", "eparchyCode": "971"},
        "pageSize": 10,
        "pageNum": 1}
    results = requests.post(url, params=params, json=payload).status_code
    print(results)


if __name__ == '__main__':
    code_read()
    print(code_read())
    c = Counter()
    print(c.count(), c.count(), c.count())
    for i in range(2):
        print(OrgCode())
    post_check('http://10.124.146.175/cust-web/cust/CustInfoController/qryCustInfoList.do')

