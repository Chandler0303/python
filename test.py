from appium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
#cn.damai
 
# 连接移动设备所必须的参数
desired_caps = {
  'platformName': 'Android',  # 被测手机是安卓
    'platformVersion': '7.1.2',  # 手机安卓版本
    'deviceName': '127.0.0.1:62001',  # 设备名，安卓手机可以随意填写
    'appPackage': 'cn.damai',  # 启动APP Package名称
    'appActivity': '.homepage.MainActivity',  # 启动Activity名称
    # 'app': 'E:/data/app/com.tencent.mm-1/base.apk',
    'unicodeKeyboard': True,  # 使用自带输入法，输入中文时填True
    'resetKeyboard': True,  # 执行完程序恢复原来输入法
    'noReset': True,  # 不要重置App，如果为False的话，执行完脚本后，app的数据会清空，比如你原本登录了，执行完脚本后就退出登录了
    'newCommandTimeout': 6000,
    'automationName': 'UiAutomator2'
}
 
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
 

order = 'adb shell "dumpsys window | grep mCurrentFocus"'
pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
print(pi.stdout.read())
# time.sleep(3)
# driver.find_element(By.ID, 'cn.damai:id/homepage_header_search_btn').click()
# time.sleep(3)
# print(driver.page_source)
# driver.find_element(By.ID, 'cn.damai:id/header_search_v2_input').send_keys('安溥')
# print(123456)
 
# # 关闭app
# driver.close_app()
# # 释放资源
# driver.quit()