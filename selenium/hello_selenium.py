# coding = 'utf-8'
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
browser = webdriver.Chrome()
browser.get('http://www.google.com')
browser.implicitly_wait(30)
browser.set_page_load_timeout(30)
print('before maxmize:',browser.get_window_size())
browser.maximize_window()
sleep(2)
print('after maxmize:',browser.get_window_size())
browser.refresh()
sleep(2)
print('当前界面标题：',browser.title)
print('当前URL:',browser.current_url)
sleep(2)
browser.get('http://www.yahoo.com')
print('当前界面标题：',browser.title)
print('当前URL',browser.current_url)
browser.implicitly_wait(30)
browser.back()
browser.implicitly_wait(30)
browser.forward()
sleep(3)

browser.quit()
