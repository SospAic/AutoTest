import json
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def main():
    driver.find_element_by_id('loginUserCode').send_keys('superadmin')
    driver.find_element_by_id('loginPassword').send_keys('bss!1122')
    driver.find_element_by_name('verifyCode').click()
    print('请输入验证码')
    time.sleep(10)
    driver.find_element_by_xpath('//button[contains(text(),"新版集中集客")]').click()
    try:
        time.sleep(5)
        title = driver.find_element_by_xpath(
            '/html/body/div[1]/div/section[1]/header/div/div[2]/div[2]/span').text  # 获取登录标识
        assert title.find('管理系统')
        print('登录成功')
    except NoSuchElementException:
        driver.refresh()
        main()
        print('登录失败，重新获取Session')


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r"D:\Software\ChromePortable\chromedriver.exe")  # Chrome配置参数
    driver.get('http://10.124.166.82/portal-web/index.jsp')
    print('打开页面')
    driver.implicitly_wait(10)
    driver.maximize_window()
    main()
    cookies = driver.get_cookies()
    f1 = open('./input_file/cookie.txt', 'w')
    f1.write(json.dumps(cookies))
    f1.close()
    print(cookies)
    print('获取成功，正在退出')
    time.sleep(2)
    driver.quit()
