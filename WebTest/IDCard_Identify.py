# -*- coding: utf-8 -*-
import base64
import urllib.parse
import urllib.request


# 图片编码为base64
def base64_encode(input_name, output_name):
    with open(input_name, 'rb') as fin:
        image_data = fin.read()
        print(image_data)
        base64_data = base64.b64encode(image_data)
        print(base64_data)
        fout = open(output_name, 'w')
        fout.write(base64_data.decode())
        fout.close()


# base64 解码为图片
def base64_decode(input_name, output_name):
    with open(input_name, 'r') as fin:
        base64_data = fin.read()
        ori_image_data = base64.b64decode(base64_data)
        fout = open(output_name, 'wb')
        fout.write(ori_image_data)
        fout.close()


def get_identify(url):
    # url = 'http://localhost/login.php'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/' \
                 '537.36 (KHTML, like Gecko) Chrome/72.0.3622.0 Safari/537.36'
    values = {'act': 'login', 'login[email]': 'abc@abc.com', 'login[password]': '123456'}
    headers = {'User-Agent': user_agent,
               'Content-Type': 'application/x-www-from-urlencoded',
               'Accept': 'application/json, text/javascript, */*; q=0.01'}
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print(the_page.decode("utf8"))


"""
在Python3中，将中文进行urlencode编码使用函数
urllib.parse.quote(string, safe='/', encoding=None, errors=None)
而将编码后的字符串转为中文，则使用
urllib.parse.unquote(string, encoding='utf-8', errors='replace')
"""

if __name__ == '__main__':
    base64_encode(r'C:\Users\Administrator\Desktop\timg.jpg', r'C:\Users\Administrator\Desktop\base64_content.txt')
    base64_decode(r'C:\Users\Administrator\Desktop\base64_content.txt', r'C:\Users\Administrator\Desktop\out.jpg')
    # base64 转码为urlencode    urllib.parse.quote(string, safe='/', encoding=None, errors=None)
    file = open(r'C:\Users\Administrator\Desktop\base64_content.txt', 'r').read()
    print(file)
    ur = urllib.parse.quote(file)  # urlcode编码
    print('urlcode编码：', ur)
    ur2 = urllib.parse.unquote(ur)  # urlcode解码
    print('urlcode解码：', ur2)
