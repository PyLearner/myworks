__author__ = 'myang'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from time import sleep



#测试百度云上传文件
username = 'yy132825'
password = '518918'
url = 'http://yun.baidu.com'


#启动浏览器并打开百度云网站并智能等待30秒
browser = webdriver.Firefox()
# browser = webdriver.Ie()
browser.get(url)
browser.implicitly_wait(30)
browser.maximize_window()
#定位登录框
loginform = browser.find_element_by_css_selector('div#sysLoginForm>form>p:nth-child(3)>input')
loginform.click()
loginform.clear()
loginform.send_keys(username)
#定位密码框
loginform = browser.find_element_by_css_selector('div#sysLoginForm>form>p:nth-child(4)>input')
loginform.click()
loginform.clear()
loginform.send_keys(password)
#定位登录按钮
loginform = browser.find_element_by_css_selector('div#sysLoginForm>form>p:nth-child(7)>input')
loginform.click()
sleep(2)

#登陆之后，找到网盘 并点击
disk = browser.find_element_by_css_selector('div.navs>div>a.pulldown-nav')
ActionChains(browser).move_to_element(disk).click_and_hold(disk).perform()
disk1 = browser.find_element_by_css_selector('div.navs div.content>a:nth-child(1)')
ActionChains(browser).move_to_element(disk1).click().perform()
sleep(10)

#进入之后，弹出对话框，先关掉它
browser.find_element_by_css_selector('a[title="关闭"]').click()
#进入之后点击上传文件

# upload = browser.find_element_by_css_selector('div.module-toolbar span>div.global-uploader')
upload = browser.find_element_by_css_selector('div.module-toolbar span>a#upload>span.text')

# print('please:',upload.text)
file = "d:\vrrp.jpg"
upload.send_keys(file)
sleep(10)


#退出浏览器
browser.quit()



