import urllib.request
import json
import pymysql
import requests
from PIL import Image
from requests import cookies


class MySQLConnect:
    def __init__(self, host="涉密未填写", name="涉密未填写", pwd="涉密未填写", table="涉密未填写"):
        self.host = host
        self.name = name
        self.pwd = pwd
        self.table = table

    def sql_execute(self, sql):
        db = pymysql.connect(self.host, self.name, self.pwd, self.table)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取字段名
            index = cursor.description
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                for c in range(0, len(index)):
                    print(str(index[c][0]) + ' = ' + str(row[c]))
        except:
            print('未查询到指定数据')
        # 关闭数据库连接
        db.close()


def get_cookie(file='./input_file/cookie.txt'):
    f2 = open(file)
    cookie = f2.read()
    cookie = json.loads(cookie)
    cookies = []
    for c in cookie:
        cookies.append(c)
    return cookies


def request_get(url_add, request_data):
    # loginUrl = url_add
    # postData = request_data
    rs = s.post(url_add, request_data)
    print(rs.status_code)


def login_check(url):
    urllib.request.urlretrieve('http://10.124.156.55/portal-web/portal/LoginController/vcode.do?1554363712307',
                               './out_img/interface.jpg')
    im = Image.open('./out_img/interface.jpg')
    im.show()
    code = input('请输入验证码：')
    loginUrl = url
    postData = {"userCode": "superadmin", "password": "gbgbhdfpdbdbdcdc", "verifyCode": code, "clientType": "1000",
                "browserType": "Chrome", "loginWay": "password"}
    rs = s.post(loginUrl, postData)
    c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
    c.set('cookie-name', 'cookie-value')
    s.cookies.update(c)
    print(rs.status_code)


if __name__ == '__main__':
    s = requests.session()
    login_check('http://10.124.156.55/portal-web/portal/LoginController/login.do')
    request_get('http://10.124.156.55/portal-web/portal/LogClickEventController/menuClickEventLog.do',
                '{menuId: "2111", menuName: "客户资料管理", clickedTime: "2019-04-04 16:42:28 886"}'.encode('utf-8'))
