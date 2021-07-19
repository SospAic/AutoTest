# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File Name：   Get_IDS_Rules
  Description :
  Author :    Adonet
  date：     2021/07/14
-------------------------------------------------
  Change Activity:
          2021/07/14:
-------------------------------------------------
"""
__author__ = 'adonet'

import os
import re
import threading
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning, ProtocolError

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)  # 在执行函数的同时，把结果赋值给result,然后通过get_result函数获取返回的结果

    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None


class GetRules:
    def __init__(self, begin_num, end_num, url):
        self.count = 0
        self.url = url
        self.failed_num = []
        self.begin_num = begin_num
        self.end_num = end_num
        self.connect = requests.session()
        self.connect.keep_alive = False  # 关闭保持连接（非常重要）
        self.login_address = '{}/user/login'.format(self.url)
        self.login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
        }
        self.login_data = {
            'user[account]': 'lt_ns_2020',
            'user[password]': '3fceb2b167f59d13333ae1a5d5424884fd35344a1735f567fd207a52'
                              '46aac9fad2af1743ea28427cf22ac64553ebd1edb1dbc38b55519f3d'
                              '8d2ca161eac8cb876f64856c49f71db7aabe27631c9c74c8fe3cc250'
                              '597302c8de2f47d00014c85357f5ef6253c90ed5158f0fab94743114'
                              '3a90cd675a1628c97f2e4eaf7cbda2fe57cf0c20d3317306acd2b6e3'
                              '2e1ef36ef2254d8ce979850d1dd021574fb1e7b6def3b5b214f46347'
                              '82238c6da12e425ed354444499aa3140470d0bf7ffd7e5181f7fa70a'
                              '8d2fbfaa09ad1d4c57c3d2a75e8be0c05689473e718b8e80da344f21'
                              'bf51dc9417a5ab6b8dead9cb1930cf2ca4b85bd9fda03e4134a8783b'
                              'b3647f53 ',
            'lang': 'zh_CN',
            'user[token]': ''
        }

    def auto_login(self):
        rs = self.connect.post(self.login_address, headers=self.login_header, data=self.login_data, verify=False)
        # print(rs.headers, rs.text, rs.content.decode('UTF-8'))
        rs1 = self.connect.get('https://10.199.172.201:4443/', headers=self.login_header, verify=False)
        self.login_header['Cookie'] = rs1.request.headers['Cookie']

    def normal_login(self):
        self.login_header['Cookie'] = ''
        rs = self.connect.get('https://10.199.172.201:4443/', headers=self.login_header, verify=False)
        print(self.login_header, rs.content.decode('UTF-8'))

    def content(self, create_num):
        url_add = 'https://10.199.172.201:4443/help/showrule/id/{}'.format(create_num)
        rs = self.connect.get(url_add, headers=self.login_header, verify=False)
        try:
            content_details = rs.content.decode('UTF-8')
            title_base = re.findall(r'<h4>(.+?)</h4>', content_details)
            self.title = title_base[0]
            file_name = re.sub(r'[\\/:*?\"<>|]', '_', self.title)
            current_path = './rules/'
            if os.path.exists(current_path):
                pass
            else:
                os.makedirs(current_path)
            file_save = open("{}{}_{}.html".format(current_path, create_num, file_name), "w", encoding='UTF-8')
            file_save.write(content_details)
            file_save.close()
            return 1
        except UnicodeDecodeError:
            # content_details = rs.content.decode('gb18030')
            return 0
        except IndexError:
            print('添加{}出错，请检查'.format(create_num))
            self.failed_num.append(create_num)
            return 0
        except OSError:
            print('添加{}出错，请检查'.format(create_num))
            self.failed_num.append(create_num)
            return 0

    def create_thread(self):
        for create_num in range(self.begin_num, self.end_num):
            # print(create_num)
            get_start = MyThread(func=self.content, args=(create_num,))
            get_start.run()
            # print(get_start.get_result())
            if get_start.get_result():
                print('成功添加一条：{}：{}'.format(create_num, self.title))
                self.count += 1
        print('创建完成，总计添加{}条\n创建失败详情：{}'.format(self.count, self.failed_num))


if __name__ == '__main__':
    begin_num = 10000
    end_num = 80000
    get_rule = GetRules(begin_num, end_num, 'https://10.199.172.201:4443')
    get_rule.auto_login()
    # get_rule.normal_login()
    get_rule.create_thread()
