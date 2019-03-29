from pytesseract import *
from PIL import Image
from PIL import ImageEnhance
import re


def randomCodeOcr(filename='./pic_code/authcode.png'):
    image = Image.open(filename)
    image = image.convert("L")  # 调用Image对象下的convert()方法，传入L。表示将彩色图像转换为灰度图像
    threshold = 130  # 指定二值化的阙值
    table = []
    for i in range(256):  # 根据调色板的默认颜色数遍历
        if i < threshold:  # 根据比指定阙值大和小分别添加二值化数字到列表
            table.append(0)
        else:
            table.append(1)
    # 使用ImageEnhance可以增强图片的识别率
    enhancer = ImageEnhance.Contrast(image).enhance(4)
    # enhancer = enhancer.enhance(4)
    # 调用Image对象下的point()方法传入包含256个频段的二值化列表对图片进行处理，"1"为输出模式的一种
    # image = image.point(table, "1")
    # 调用Image对象下的show()方法展示图片
    image.show()
    ltext = ''
    ltext = image_to_string(image)
    # 去掉非法字符，只保留字母数字
    ltext = re.sub("\W", "", ltext)
    print(u'[%s]识别到验证码:[%s]!!!' % (filename, ltext))
    image.save(filename)
    return ltext


if __name__ == '__main__':
    randomCodeOcr()
