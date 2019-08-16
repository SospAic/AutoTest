# -*- coding: utf-8 -*-

import requests
import traceback


# POST URL image
def post_url(image_url):
    crop_image = "0"
    type = "0"
    api_url = "https://fapiao.exocr.com/ocr/v2/fapiao"
    # image_url = ""
    result = {}
    try:
        # post request
        data = {'image_url': image_url, 'crop_image': crop_image, 'type': type}
        r = requests.post(api_url, data=data)
        if r.status_code != 0:
            print("failed to get info from : ", image_url)
        else:
            result = r.json()
            print(result)
    except:
        traceback.print_exc()
    return result


# POST Base64 image
def post_base64(str_base64):
    crop_image = "0"
    type = "0"
    api_url = "https://fapiao.exocr.com/ocr/v2/fapiao"
    result = {}
    try:
        # post request
        data = {'image_base64': str_base64, 'crop_image': crop_image, 'type': type}
        r = requests.post(api_url, data=data)
        if r.status_code != 0:
            print("failed to get info from base64 ")
        else:
            result = r.json()
            print(result)
    except:
        traceback.print_exc()
    return result


# POST Binary image
def post_binary(image_path):
    crop_image = "0"
    type = "0"
    api_url = "https://fapiao.exocr.com/ocr/v2/fapiao"
    result = {}
    try:
        # post request
        with open(image_path, 'rb') as f:
            binary_data = f.read()
        data = {'image_binary': binary_data, 'crop_image': crop_image, 'type': type}
        r = requests.post(api_url, data=data)
        if r.status_code != 0:
            print("failed to get info from base64 ")
        else:
            result = r.json()
            print(result)
    except:
        traceback.print_exc()
    return result


if __name__ == '__main__':
    post_url("http://s13.sinaimg.cn/bmiddle/001AMq7Ezy7bO6YESTy0c&690")
