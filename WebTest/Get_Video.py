# -*- coding:utf-8 -*-
import os
import sys
import requests
import datetime
from Crypto.Cipher import AES
from Crypto import Random
import json
from binascii import b2a_hex, a2b_hex

# 这个地址需要手工抓包获得
m3u8_url = 'https://vedu.csdn.net/media/m3u8_new_tmp/10085/2253d7de848351de21e59953dec373a4-215004.m3u8'

# 每个视频播放前都会有个广告，这个也要手工抓取，获取token必须用广告地址
guanggao_url = 'https://vedu.csdn.net/media/adv_new_tmp/5s/38911d59c8bb154fa3c4226baf3ca813-6.m3u8'


def get_pid():
    return 'pid-1-5-1'


def get_token():
    # 这个是获取广告的token
    # token_url = 'https://edu.csdn.net/bcscloud/course_video/get_start_token?url='+guanggao_url
    # return json.loads(requests.get(token_url).text).get('token')

    # 后边的/10085/215004是在网页地址栏里，没办法，手工获取吧
    token_url = 'https://edu.csdn.net/bcscloud/course_video/get_token/10085/215004'
    return json.loads(requests.get(token_url).text).get('token')


def get_key(key_url):
    key_url_all = key_url + '&playerId=' + get_pid() + '&token=' + get_token()
    return json.loads(requests.get(key_url_all).text).get('encryptedVideoKey')


def download(url):
    download_path = os.getcwd() + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # 新建日期文件夹
    download_path = os.path.join(download_path, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    download_path_encode = download_path + '_encode'
    download_path_decode = download_path + '_decode'
    os.mkdir(download_path_encode)
    os.mkdir(download_path_decode)

    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    if "#EXTM3U" not in all_content:
        raise BaseException("非M3U8的链接")

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                all_content = requests.get(url).text

    file_line = all_content.split("\n")

    unknow = True
    key = ""
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print("Decode Method：", method)

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
            key = get_key(key_path)
            print("key：", key)

        if "EXTINF" in line:  # 找ts地址并下载
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]  # 拼出ts片段的URL
            # print pd_url

            res = requests.get(pd_url)
            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]

            if len(key):  # AES 解密
                iv = Random.new().read(AES.block_size)
                cryptor = AES.new(key.encode('utf-8'), AES.MODE_CBC)
                with open(os.path.join(download_path_decode, c_fule_name + ".mp4"), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
                # else:
                with open(os.path.join(download_path_encode, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
    if unknow:
        raise BaseException("未找到对应的下载链接")
    else:
        print("下载完成")

    merge_file(download_path_decode)


def merge_file(path):
    os.chdir(path)
    os.system("copy /b * new.tmp")
    # os.system('del /Q *.ts')
    # os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")


if __name__ == '__main__':
    download(m3u8_url)
