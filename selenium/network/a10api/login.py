__author__ = 'myang'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

class GuiLogin():
    browser = ''
    def __init__(self,ax_ip,ax_user,ax_password,browser_type):
        self.ax_ip = ax_ip
        self.ax_user = ax_user
        self.ax_password = ax_password
        self.browser_type = browser_type
        # self.browser = browser
    def constructUrl(self, ax_ip):
        self.url = r'http://' + ax_ip
        return self.url
    def guiLogin(self):
        if self.browser_type.upper() == 'FIREFOX':
            self.browser = webdriver.Firefox()
        elif self.browser_type.upper() == 'CHROME':
            self.browser = webdriver.Chrome()
        elif self.browser_type.upper() == 'IE':
            self.browser = webdriver.Ie()
        self.browser.implicitly_wait(30)
        # 定位username框
        self.browser.get(self.constructUrl(self.ax_ip))
        self.browser.find_element_by_css_selector('div.input>input#id_username').click()
        self.browser.find_element_by_css_selector('div.input>input#id_username').clear()
        self.browser.find_element_by_css_selector('div.input>input#id_username').send_keys(self.ax_user)
        # 定位密码框
        self.browser.find_element_by_css_selector('div.input>input#id_password').click()
        self.browser.find_element_by_css_selector('div.input>input#id_password').clear()
        self.browser.find_element_by_css_selector('div.input>input#id_password').send_keys(self.ax_password)
        # 定位下拉语言选择框
        select = Select(self.browser.find_element_by_css_selector('div.input>select#id_language'))
        # select.deselect_all()
        select.select_by_value('zh-cn')
        # time.sleep(5)
        #定位登录按钮
        self.browser.find_element_by_css_selector('p>button.btn.btn-primary.btn-block').send_keys(Keys.RETURN)
        sleep(2)
        return(self.browser)

    def guiLogout(self):
        self.browser.quit()

    def moveToADC_Slb(self):
        self.browser.maximize_window()
        a1 = self.browser.find_element_by_css_selector('div#a10-menu-bar>div>ul>li:nth-child(2)')
        # ActionChains(self.browser).move_to_element(a1).click_and_hold(a1).perform()
        ActionChains(self.browser).move_to_element(a1).perform()
        slb = self.browser.find_element_by_css_selector('div#a10-menu-bar>div>ul>li:nth-child(2)>ul>li:nth-child(1)>a')
        ActionChains(self.browser).move_to_element(slb).click().perform()

    def moveToADC_Templates(self):
        self.browser.maximize_window()
        adc = self.browser.find_element_by_css_selector('div#a10-menu-bar>div>ul>li:nth-child(2)>a>span')
        ActionChains(self.browser).move_to_element(adc).perform()
        # ActionChains(self.browser).move_to_element(adc).perform()
        sleep(1)
        templates = self.browser.find_element_by_css_selector('div#a10-menu-bar>div>ul>li:nth-child(2)>ul>li:nth-child(3)>a')
        ActionChains(self.browser).move_to_element(templates).click().perform()

        sleep(2)


