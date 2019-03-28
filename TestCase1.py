from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# driver = webdriver.Firefox(firefox_binary="D:\\Software\\Mozilla Firefox\\firefox.exe",
#                           executable_path="D:\\Software\\Mozilla Firefox\\geckodriver.exe")
# driver = webdriver.Firefox(executable_path="D:\\迅雷下载\\FirefoxPortable\\App\\Firefox64\\firefox.exe")
driver = webdriver.Chrome(executable_path="D:\\Software\\ChromePortable\\chromedriver.exe")
# driver = webdriver.Ie(executable_path="C:\\Windows\\System32\\IEDriverServer.exe")
driver.implicitly_wait(2)
driver.get('http://132.42.43.117/ulp/')
time.sleep(2)
driver.find_element_by_id("username").clear()
driver.find_element_by_id("username").send_keys("hefei")
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys("abc@123")

driver.add_cookie(cock)  # 这里添加cookie，有时cookie可能会有多条，需要添加多次
time.sleep(3)

# 刷新下页面就可以看到登陆成功了
driver.refresh()

# try:
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))

# driver = webdriver.Firefox()
# driver.switch_to.frame(0)  # 1.用frame的index来定位，第一个是0
# driver.switch_to.frame("frame1")  # 2.用id来定位
# driver.switch_to.frame("myframe")  # 3.用name来定位
# driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # 4.用WebElement对象来定位

# finally:
# driver.quit()
