# coding='utf-8'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from time import sleep

browser = webdriver.Firefox()

url = 'http://www.mi.com'
username = '1587617118@qq.com'
password = 'jiayou518'

browser.get(url)
browser.implicitly_wait(30)
#print(browser.find_element_by_link_text('登录').text)
#首页找到 登录
browser.find_element_by_link_text('登录').click()

#输入信息并登录
browser.find_element_by_id('miniLogin_username').click()
browser.find_element_by_id('miniLogin_username').clear()
browser.find_element_by_id('miniLogin_username').send_keys(username)
browser.find_element_by_id('miniLogin_pwd').click()
browser.find_element_by_id('miniLogin_pwd').clear()
browser.find_element_by_id('miniLogin_pwd').send_keys(password)

#提交
#browser.find_element_by_id('message_LOGIN_IMMEDIATELY').send_keys(Keys.ENTER)
browser.find_element_by_id('message_LOGIN_IMMEDIATELY').submit()
browser.implicitly_wait(30)
sleep(5)

login_name = browser.find_element_by_xpath("//b[@class='user-name']")
ActionChains(browser).move_to_element(login_name).perform()
person_center = browser.find_element_by_xpath("//a[contains(text(),'个人中心')]")
ActionChains(browser).move_to_element(person_center).click().perform()
browser.set_page_load_timeout(30)
browser.implicitly_wait(30)
print('current_url: ',browser.current_url)
#browser.maximize_window()
#print('info:', browser.find_element_by_xpath("//div[@class='uc-info']/h3/span").text)
##userinfo = u'lhyaxian'
##if browser.find_element_by_class_name("//h3[@class='user-name']/span").text == userinfo:
##        print('login successfully,' + userinfo + '.')

sleep(5)
browser.quit()


#welcome = u'欢迎您'

#print('user : ',browser.find_element_by_xpath("//b[@class='user-name']").text)
##if browser.find_element_by_xpath("//div[@class='container']/div/div").text == welcome:
##    if browser.find_element_by_class_name('user-name').text == 'lhyaxian':
##        print('登陆成功 !' + '欢迎您 ' + 'lhyaxian')




#browser.find_element_by_id('message_LOGIN_IMMEDIATELY')

#browser.quit()
