from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from a10networks.a10api.login import GuiLogin
import os
import unittest
from time import sleep
ax_ip = '192.168.102.226'
ax_user = 'admin'
ax_password='a10'

class TestSlbServer(unittest.TestCase):
    driver=''
    login = ''
    def setUp(self):
        #browser_type should be one of ['firefox','chrome','ie']
        self.login = GuiLogin(ax_ip=ax_ip,ax_user=ax_user,ax_password=ax_password,browser_type='firefox')
        self.driver = self.login.guiLogin()
        self.login.moveToADC_Slb()
        sleep(2)

    def tearDown(self):
        self.login.guiLogout()

    def createServer(self,servername, serverip,screenshotname):
        #create server 点击create按钮
        self.driver.find_element_by_css_selector('div.panel-body div.form-group>a:nth-child(7)').click()
        #进入创建server页面
        server_name = self.driver.find_element_by_css_selector('div.formFieldDiv>div>div:nth-child(1)>div>input')
        server_name.click()
        server_name.clear()
        server_name.send_keys(servername)
        #ipv4 address 是默认选中的，所以没必要再选一次 ip-type的三个 radiobox是按照顺序排列的，1:ipv4 2:ipv6 3:fqdn
        # server_ip_type = self.driver.find_element_by_css_selector('div.formFieldDiv>div>div:nth-child(2) ul>li:nth-child(1)')
        # server_ip_type.click()
        server_ip = self.driver.find_element_by_css_selector('div.formFieldDiv>div>div:nth-child(3)>div>input')
        server_ip.click()
        # server_ip.clear()
        server_ip.send_keys(serverip)
        #点击create按钮进入real port 创建页面
        self.driver.find_element_by_css_selector('table#Port>thead>tr:nth-child(1) a').click()
        server_port_num = self.driver.find_element_by_css_selector('div.formFieldDiv>div>div:nth-child(1)>div>input')
        # server_port_num.click()
        # server_port_num.clear()
        server_port_num.send_keys(80)
        #注释掉是因为默认就是TCP ，如果需要用UDP 只需要 修改 为 UDP
        # server_port_proto = Select(self.driver.find_element_by_css_selector('div.formFieldDiv>div>div:nth-child(2)>div>select'))
        # server_port_proto.select_by_visible_text('TCP')

        #定位create 按钮来创建配置玩的port
        self.driver.find_element_by_css_selector('div.panel-body>div:nth-child(2)>div>input').click()

        #从port页面重新转到server创建页面，定位 update按钮来完成创建server的过程
        self.driver.find_element_by_css_selector('div.panel-body>div:nth-child(2)>div>input').click()
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'screenshot')
        self.driver.get_screenshot_as_file(os.path.join(base_dir,screenshotname))

    def testSlbServer(self):
        #定位server
        server = self.driver.find_element_by_css_selector('div#main-page ul>li:nth-child(4)>a')
        server.click()
        sleep(2)
        for i in range(1,3):
            server_name = 'Create_server_%s' % i
            server_ip = '23.1.1.%s' % i
            screenshotname = 'Create_server_%s.jpg' % i
            self.createServer(server_name,server_ip,screenshotname)
        #判断是否创建成功 检查 server name，ip


if __name__ == '__main__':
    unittest.main()

