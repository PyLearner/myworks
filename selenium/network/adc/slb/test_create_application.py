__author__ = 'myang'

from a10networks.a10api.login import GuiLogin
import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.common.action_chains import ActionChains
ax_ip = '192.168.102.226'
ax_username = 'admin'
ax_password = 'a10'

# 全局变量 driver = ''
class CreateApplication(unittest.TestCase):
    driver = ''
    def setUp(self):
        # global driver
        login =  GuiLogin(ax_ip,ax_username,ax_password)
        self.driver = login.guiLogin()


    def testCreateApplication(self):
        print('it could work !')
    def tearDown(self):
        # global driver
        self.driver.quit()
        print('successfully quit !')







