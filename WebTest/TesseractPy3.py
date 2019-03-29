# coding=utf-8

import os
import subprocess
import traceback
import logging

from PIL import Image  # 来源于Pillow库

TESSERACT = './other/tesseract'  # 调用的本地命令名称
TEMP_IMAGE_NAME = "temp.bmp"  # 转换后的临时文件
TEMP_RESULT_NAME = "temp"  # 保存识别文字临时文件
CLEANUP_TEMP_FLAG = True  # 清理临时文件的标识
INCOMPATIBLE = True  # 兼容性标识


def image_to_scratch(image, TEMP_IMAGE_NAME):
    # 将图片处理为兼容格式
    image.save(TEMP_IMAGE_NAME, dpi=(200, 200))


def retrieve_text(TEMP_RESULT_NAME):
    # 读取识别内容
    inf = open(TEMP_RESULT_NAME + '.txt', 'r')
    text = inf.read()
    inf.close()
    return text


def perform_cleanup(TEMP_IMAGE_NAME, TEMP_RESULT_NAME):
    # 清理临时文件
    for name in (TEMP_IMAGE_NAME, TEMP_RESULT_NAME + '.txt', "tesseract.log"):
        try:
            os.remove(name)
        except OSError:
            pass


def call_tesseract(image, result, lang):
    # 调用tesseract.exe，将识读结果写入output_filename中
    args = [TESSERACT, image, result, '-l', lang]
    proc = subprocess.Popen(args)
    retcode = proc.communicate()


def image_to_string(image, lang, cleanup=CLEANUP_TEMP_FLAG, incompatible=INCOMPATIBLE):
    # 假如图片是不兼容的格式并且incompatible = True，先转换图片为兼容格式（本程序将图片转换为.bmp格式），然后获取识读结果;如果cleanup=True,操作之后删除临时文件。
    logging.basicConfig(filename='tesseract.log')
    try:
        try:
            call_tesseract(image, TEMP_RESULT_NAME, lang)
            text = retrieve_text(TEMP_RESULT_NAME)
        except Exception:
            if incompatible:
                image = Image.open(image)
                image_to_scratch(image, TEMP_IMAGE_NAME)
                call_tesseract(TEMP_IMAGE_NAME, TEMP_RESULT_NAME, lang)
                text = retrieve_text(TEMP_RESULT_NAME)
            else:
                raise
        return text
    except:
        s = traceback.format_exc()
        logging.error(s)
    finally:
        if cleanup:
            perform_cleanup(TEMP_IMAGE_NAME, TEMP_RESULT_NAME)
