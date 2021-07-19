from aip import AipOcr


# 文字识别高精度版本
class BaiduAip:
    def __init__(self, filePath, image_time):
        self.filePath = filePath
        self.image_time = image_time

    def get_file_content(self):
        with open(self.filePath, 'rb') as fp:
            return fp.read()

    def image_ocr(self):
        APP_ID = '24107714'
        API_KEY = 'guKhh1ICHk3oFjoxWQZS8jIS'
        SECRET_KEY = 'cAvRRxhIO19dONgQSfftTDyRsSOR7N5t'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        image = self.get_file_content(self.image_time)
        # 调用通用文字识别（高精度版） """
        client.basicAccurate(image)
        # 如果有可选参数 """
        options = dict()
        options["detect_direction"] = "false"
        options["probability"] = "true"
        options["language_type"] = "ENG"
        # 带参数调用通用文字识别（高精度版） """
        data_ocr = client.basicAccurate(image, options)
        print(data_ocr)
        data_ocr = data_ocr["words_result"][0]["words"].replace(" ", "") if data_ocr["words_result"] else list()
        return data_ocr


if __name__ == '__main__':
    baidu_ocr = BaiduAip('./pic_code/code.jpg')
    baidu_ocr.image_ocr()
