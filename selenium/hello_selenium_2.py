from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os,time

driver = webdriver.Firefox()

driver.get("http://www.baidu.com")

#输入框输入内容
driver.find_element_by_id("kw").send_keys("gui")
time.sleep(3)

#ctrl+a 全选输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')
time.sleep(3)

#ctrl+x 剪切输入框内容
driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'x')
time.sleep(3)

#输入框重新输入内容，搜索
driver.find_element_by_id("kw").send_keys(u"虫师 cnblogs")
driver.find_element_by_id("su").click()

time.sleep(3)
driver.quit()
