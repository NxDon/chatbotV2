from selenium import webdriver  # 导入库
import time
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import xlrd


class ChatBot:
    def __init__(self, driverPath, options):
        self.mainPageURL = 'https://www.amazon.co.uk'
        self.mainWindowHandle = ''
        self.cookie = ''
        self.driver = webdriver.Chrome(driverPath, chrome_options=options)
        self.wait = WebDriverWait(self.driver, 5, 0.5)
        self.adText="Hi!!!!"

    def openMainPage(self, ck):
        self.driver.get(self.mainPageURL)
        self.mainWindowHandle = self.driver.current_window_handle
        # do load cookie and stuff
        # with open(ck, 'r') as f:
        #     listCookies = json.loads(f.read())
        #     for cookie in listCookies:
        #         self.driver.add_cookie(cookie)
        #     # 读取完cookie刷新页面
        # time.sleep(1)
        # self.driver.get(self.mainPageURL)

    def openGoodPage(self, url):
        print("STEP 1 打开商品页面")
        self.driver.get(url)
        self.wait.until(ec.presence_of_element_located((By.ID, "wishListMainButton-announce")))
        print("商品页面加载完成,检测是否是第三方卖家")

    def getSellerBtn(self):
        print("STEP 2 判断是否是三方卖家")
        try:
            seller = self.driver.find_element_by_id("sellerProfileTriggerId")
        except Exception:
            print(Exception)
            return False
        print("是三方卖家")
        return seller

    def openSellerPage(self, sellerBtn):
        sellerBtn.click()
        self.wait.until(ec.presence_of_element_located((By.ID, "seller-contact-button")))


    def isChineseSeller(self):
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".a-unordered-list.a-nostyle.a-vertical")))
        sellerInfo = self.driver.find_element_by_css_selector(".a-unordered-list.a-nostyle.a-vertical")
        return sellerInfo.text.find("CN") != -1

    def getContactBtn(self):
        self.wait.until(ec.presence_of_element_located((By.ID, "seller-contact-button")))
        return self.driver.find_element_by_id("seller-contact-button")

    def openChatPage(self,contactBtn):
        contactBtn.click()

    def switchToChatWindow(self):
        cur_handles = self.driver.window_handles
        self.wait.until(ec.new_window_is_opened(cur_handles))
        # 再次获取所有的窗口
        # 获取所有的窗口，句柄
        all_handles = self.driver.window_handles
        # 切换到新打开的窗口
        self.driver.switch_to.window(all_handles[-1])
        print("切换到聊天窗口")

    def skipChat(self):
        self.wait.until(ec.presence_of_element_located((By.XPATH, "//li[contains(text(),'An item')]")))
        chat1 = self.driver.find_element_by_xpath("//li[contains(text(),'An item')]")
        chat1 = chat1[-1]
        chat1.click()
        self.wait.until(ec.presence_of_element_located((By.XPATH, "//li[contains(text(),'Other')]")))
        chat2 = self.driver.find_element_by_xpath("//li[contains(text(),'Other')]")
        chat2.click()


    def sendAdMessage(self):
        self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".textarea-input")))
        textArea = self.driver.find_element_by_css_selector(".textarea-input")
        textArea.send_keys(self.adText)

    def closeOtherWindow(self):
        print("发送完成，关闭其他所有界面")
        #获得当前所有打开的窗口句柄
        cur_handle = self.driver.current_window_handle
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != self.mainWindowHandle:
                self.driver.switch_to.window(handle)
                self.driver.close()


    def startChating(self, goodURL):
        self.openGoodPage(goodURL)
        sellerBtn = self.getSellerBtn()
        if sellerBtn:
            self.openSellerPage()
            if self.isChineseSeller():
                chatBtn = self.getContactBtn()
                self.openChatPage(chatBtn)
                self.switchToChatWindow()
                self.skipChat()
                self.sendAdMessage()
                self.closeOtherWindow()
                #返回主界面
                self.driver.switch_to.window(self.mainWindowHandle)




