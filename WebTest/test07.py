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

import re
import time
import requests

str_a = """
<html>
<head>
<title>规则ID: 10017</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style>
td {font-family: "宋体"; font-size: 10pt; table-layout:fixed;word-break :break-all;}
body {font-family: "宋体"; font-size: 10pt}
select {font-family: "宋体"; font-size: 10pt}
a:link {text-decoration: none; color: #0000ff}
a:visited {text-decoration: none; color: #0000ff}
a:active {text-decoration: underline; color: #ff000}
a:hover {text-decoration: underline; color: #ff0000}

.grey {background-color: #c0c0c0; border: 1px outset; text-align: center; vertical-align: baseline; border-color: #FFFFFF solid; font-size: 9pt; font-style: normal}
.red {background-color: #ff0000; border: 1px outset; text-align: center; vertical-align: baseline; border-color: #FFFFFF solid; font-size: 9pt; font-style: normal}
.green {background-color: #00cc00; border: 1px outset; text-align: center; vertical-align: baseline; border-color: #FFFFFF solid; font-size: 9pt; font-style: normal}
</style>
</head>

<body background="bg.bmp" height="100%" width="100%" topmargin="0" leftmargin="0">
<table width="98%" border="0" align="center">
   <tr>
     <td colspan="2">&nbsp;</td>
   </tr>
<tr>
  <td colspan="2" align="center"><h4>Microsoft FTP服务程序STAT glob()扩展拒绝服务攻击漏洞</h4></td>
</tr>
<tr>
  <td colspan="2" align="center"><hr size="1"></td>
</tr>
<tr>
  <td nowrap><b>规 则 编 号</b>&nbsp;&nbsp;</td>
  <td width="100%">10017</td>
</tr>
<tr>
  <td nowrap><b>规则更新时间</b>&nbsp;&nbsp;</td>
  <td>2002-08-26</td>
</tr>
<tr>
  <td nowrap><b>事件所属大类</b>&nbsp;&nbsp;</td>
  <td>拒绝服务类攻击</td>
</tr>
<tr>
  <td nowrap><b>事件威胁等级</b>&nbsp;&nbsp;</td>
  <td>中</td>
</tr>
<tr>
  <td nowrap><b>事件技术手段</b>&nbsp;&nbsp;</td>
  <td>畸形攻击</td>
</tr>
<tr>
  <td nowrap><b>事件服务类型</b>&nbsp;&nbsp;</td>
  <td>FTP</td>
</tr>
<tr>
  <td nowrap><b>事件流行程度</b>&nbsp;&nbsp;</td>
  <td>低</td>
</tr>
<tr>
  <td colspan="2" align="center"><hr size="1"></td>
</tr>

<tr><td nowrap><b>相关漏洞</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>
<tr><td colspan="2"><b>漏洞标题</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2"><a href='http://www.nsfocus.net/vulndb/2610'>Microsoft FTP服务程序STAT glob()扩展拒绝服务攻击漏洞</a></td></tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr>
  <td nowrap><b>NSFOCUS ID</b>&nbsp;&nbsp;</td>
  <td><a href='http://www.nsfocus.net/vulndb/2610'>2610</a></td>
</tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr>
  <td nowrap><b>BUGTRAQ ID</b>&nbsp;&nbsp;</td>
  <td><a href='http://www.securityfocus.com/bid/4480'>4480</a></td>
</tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr>
  <td nowrap><b>CVE ID</b>&nbsp;&nbsp;</td>
  <td><a href='http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0073'>CVE-2002-0073</a></td>
</tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr>
  <td nowrap><b>CNNVD ID</b>&nbsp;&nbsp;</td>
  <td><a href='http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-200204-017'>CNNVD-200204-017</a></td>
</tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr><td colspan="2"><b>相关应用</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">Microsoft|IIS|4.0<br>Microsoft|IIS|5.0</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr><td colspan="2"><b>详细信息</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">Microsoft IIS（Internet Information Server）是MS Windows系统默认自带的Web服务器软件，其中默认包含FTP服务。 <br><br>Microsoft的FTP服务在处理STAT命令时存在问题，可导致攻击者进行拒绝服务攻击。<br><br>任何合法帐户或者匿名帐户可以在登录FTP服务程序后，提交包含各种文件扩展字符的随机数据为参数的STAT命令，可导致访问冲突产生，所有运行在inetinfo.exe进程下的服务会终止。<br><br>成功地利用这个漏洞，对于IIS 4.0其会产生拒绝服务，需要手工重新启动；对于IIS 5.0系统会自动重新启动。</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr><td colspan="2"><b>影响系统</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">Microsoft Windows|NT 4.0|<br>Microsoft Windows|2000 SP3|<br>Microsoft Windows|2000 Server SP2|<br>Microsoft Windows|2000 Server SP1|</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr><td colspan="2"><b>相关资料</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">漏洞消息：<br><br>Microsoft FTP Service STAT Globbing DoS<br>http://archives.neohapsis.com/archives/bugtraq/2002-04/0185.html</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>

<tr><td colspan="2"><b>解决方案</b>&nbsp;&nbsp;</td></tr>
<tr><td colspan="2">临时处理方法：<br><br>如果您不能立刻安装补丁或者升级，建议您采取以下措施以降低威胁：<br><br>* 暂时没有合适的临时解决方法。<br><br>厂商解决方案：<br><br>Microsoft<br>---------<br>目前厂商还没有提供补丁或者升级程序，我们建议使用此软件的用户随时关注厂商的主页以获取最新版本：<br><br>http://www.microsoft.com/</td></tr>
<tr><td colspan="2">&nbsp;</td></tr>
</html>
"""
str_b = r"""
`~!@#$%^&*()_+-=[]{}\|;:'"<,>.?/...../t\t
"""


class GetRules:
    def __init__(self, begin_num, end_num):
        self.count = 1
        self.begin_num = begin_num
        self.end_num = end_num
        self.connect = requests.session()
        self.host = '10.199.172.201:4443'
        self.login_address = 'https://10.199.172.201:4443/user/login'
        self.login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1"
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
        print(rs.headers)
        # print(rs.text, rs.content.decode('UTF-8'))
        rs1 = self.connect.get('https://10.199.172.201:4443/', headers=self.login_header, verify=False)
        self.login_header['Cookie'] = rs1.request.headers['Cookie']

    def normal_login(self):
        self.login_header['Cookie'] = ''
        rs = self.connect.get('https://10.199.172.201:4443/', headers=self.login_header, verify=False)
        print(self.login_header, rs.content.decode('UTF-8'))

    def content(self):
        for create_num in range(self.begin_num, self.end_num):
            url_add = 'https://10.199.172.201:4443/help/showrule/id/{}'.format(create_num)
            rs = self.connect.get(url_add, headers=self.login_header, verify=False)
            try:
                content_details = rs.content.decode('gb18030')
            except UnicodeDecodeError:
                content_details = rs.content.decode('UTF-8')
                file_save = open("./rules/{}.html".format(create_num), "w", encoding='UTF-8')
                file_save.write(content_details)
                file_save.close()
                print('成功添加一条：{}：')
                self.count += 1
        print('创建完成，总计添加{}条'.format(self.count))


if __name__ == '__main__':
    # get_rule = GetRules(10010, 10030)
    # get_rule.auto_login()
    # # get_rule.normal_login()
    # get_rule.content()

    a = re.findall(r'<\/?[h4]+(\s+[a-zA-Z]+=".*")*>(.+?)<\/?[h4]+(\s+[a-zA-Z]+=".*")*>', str_a)
    b = re.findall(r'<h4>(.+?)</h4>', str_a)
    c = re.findall(r'((?=[\x21-\x7e]+)[^A-Za-z0-9])', b[0])
    d = re.findall(r'[\\/:*?\"<>|]', str_b)
    e = re.sub(r'[\\/:*?\"<>|]', '_', str_b)
    # a.remove(' ')
    print(a, type(a[0]), b, c, d, e)

