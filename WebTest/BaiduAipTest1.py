# python 3.5
# 百度tesseract-ocr使用

from aip import AipOcr

""" API """
APP_ID = '24107714'
API_KEY = 'guKhh1ICHk3oFjoxWQZS8jIS'
SECRET_KEY = 'cAvRRxhIO19dONgQSfftTDyRsSOR7N5t'

# 初始化AipFace对象
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def img_to_str(image_path):
    """ 可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"  # 中英文混合
    options["detect_direction"] = "true"  # 检测朝向
    options["detect_language"] = "true"  # 是否检测语言
    options["probability"] = "false"  # 是否返回识别结果中每一行的置信度

    image = get_file_content(image_path)

    """ 带参数调用通用文字识别 """
    result = client.basicGeneral(get_file_content(filePath), options)

    # 格式化输出-提取需要的部分
    if 'words_result' in result:
        text = ('\n'.join([w['words'] for w in result['words_result']]))
    print(type(result), "和", type(text))
    print(result, text)

    # """ save """
    # fs = open("baidu_ocr.txt", 'w+')  # 将str,保存到txt
    # fs.write(text)
    # fs.close()
    return text


if __name__ == '__main__':
    filePath = './pic_code/vcode.jpg'
    print(img_to_str(filePath))
    print("识别完成。")

