# coding = utf-8

from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


desired = DesiredCapabilities.FIREFOX
browser = webdriver.Remote(command_executor='http://192.168.3.217/wd/hub',desired_capabilities=desired)
browser.start_client()

# browser.get("http://www.google.com")
browser.get("http://www.baidu.com")
browser.implicitly_wait(30)
set1 = browser.find_element_by_link_text('设置')

# print('content:',set1)
#鼠标滑动到 设置 上 ，然后 会显示下拉菜单
ActionChains(browser).move_to_element(set1).perform()

#下拉菜单出来以后，定位到’搜索设置‘并点击
set2 = browser.find_element_by_link_text('搜索设置')
ActionChains(browser).move_to_element(set2).click().perform()

m = browser.find_element_by_id('nr')
m.find_element_by_xpath("//option[@value='100']").click()

browser.find_element_by_xpath("//a[contains(text(),'保存设置')]").click()
Alert(browser).accept()
#Alert(browser).send_keys(Keys.ENTER)
#print('alert:',Alert(browser).text)
#browser.implicitly_wait(30)

time.sleep(10)
browser.find_element_by_id("kw").send_keys("gui")
browser.find_element_by_id("su").click()
time.sleep(3)

browser.quit()



"""
# browser.maximize_window()
browser.set_window_size(900,900)

browser.implicitly_wait(3)
# browser.find_element_by_id("lst-ib").send_keys("gui")
browser.find_element_by_xpath("//form[@id='form']/span/input").send_keys("gui")
# browser.find_element_by_name("btnK").click()
browser.find_element_by_id("su").click()
#browser.find_element_by_xpath("//input[@id='su']/span/input").click()
time.sleep(3)
print('当前标题:',browser.title)
print('当前URL:',browser.current_url)
browser.quit()
"""
