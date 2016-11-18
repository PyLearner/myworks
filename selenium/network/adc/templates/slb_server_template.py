__author__ = 'myang'
from a10networks.a10api.login import *
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
ax_ip = '192.168.102.226'
ax_username = 'admin'
ax_password = 'a10'

class CreateServerTemplate(unittest.TestCase):
    driver=''
    login=''
    def setUp(self):
        self.login = GuiLogin(ax_ip,ax_username,ax_password)
        self.driver = self.login.guiLogin()
        self.login.moveToADC_Templates()
        print('setUp Successfully.')

    def tearDown(self):
        self.login.guiLogout()
        print('tearDown successfully ！')

    def test1CreateServerTemplate(self):
        print('#############################################')
        print('Start to create slb server template.')
        print('#############################################')
        #定位 create 按钮
        sleep(2)
        self.driver.find_element_by_css_selector('span>button#dropdownMenu>span').click()
        print('text:',self.driver.find_element_by_css_selector('span>button#dropdownMenu>span').click())
        #定位 server
        self.driver.find_element_by_css_selector('div.form-group span>ul>li:nth-child(2)').click()
        # ActionChains(self.driver).move_to_element(server).click().perform()
        sleep(1)
        self.driver.find_element_by_css_selector('div#basicFieldsDiv>div:nth-child(1) input').send_keys('server_template_1')
        self.driver.find_element_by_css_selector('div#basicFieldsDiv>div:nth-child(2) ul>li:nth-child(2) input').click()
        sleep(1)
        self.driver.find_element_by_id('template_create_submit').click()
        self.driver.get_screenshot_as_file(r'd:\gui\a10networks\adc\templates\screenshot\after_template_create_page.jpg')
        sleep(1)

if __name__ == '__main__':
    unittest.main()







