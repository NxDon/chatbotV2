
mainSetURL = 'https://www.amazon.co.uk'
mainWindowHandle = ''
chatWindowHandle = ''

desired_capabilities = DesiredCapabilities.CHROME
#desired_capabilities["pageLoadStrategy"] = "none"
chrome_options = webdriver.ChromeOptions()
# 无窗口模式
# chrome_options.add_argument('--headless')
# 禁止硬件加速，避免严重占用cpu
chrome_options.add_argument('--disable-gpu')
# 关闭安全策略
chrome_options.add_argument("disable-web-security")
# 禁止图片加载
chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
# 隐藏"Chrome正在受到自动软件的控制
chrome_options.add_argument('disable-infobars')
# 设置开发者模式启动，该模式下webdriver属性为正常值
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
browser = webdriver.Chrome('./chromedriver',options=chrome_options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
wait = WebDriverWait(browser, 5)
#隐式等待
browser.implicitly_wait(3) # seconds


def openMainPageWithCookie(ck):
    browser.get(mainSetURL)
    time.sleep(1)
    with open(ck, 'r') as f:
        listCookies = json.loads(f.read())
        for cookie in listCookies:
            browser.add_cookie(cookie)
        # 读取完cookie刷新页面
    time.sleep(1)

    browser.get(mainSetURL)

def openGoodsProfile(good_url):
    print("打开商品页面")
    browser.get(good_url)


def getSellerBtn():
    wait.until(ec.presence_of_element_located((By.ID, "wishListMainButton-announce")))
    print("商品页面加载完成,检测是否是第三方卖家")
    try:
        seller = browser.find_element_by_id("sellerProfileTriggerId")
    except Exception:
        print("是亚马逊官方，跳过")
        return False
    print("是三方卖家")
    return seller

def openSellerProfile(sellerBtn):
    print("打开卖家信息界面")
    sellerBtn.click()
    wait.until(ec.presence_of_element_located((By.ID, "seller-contact-button")))
    chatBtn = browser.find_element_by_id("seller-contact-button")
    print("找到聊天按钮，打开聊天界面")
    chatBtn.click()


def switch_window():
    wait.until(ec.number_of_windows_to_be(2))
    print('出现两个窗口')
   # curHandle = browser.current_window_handle #获取当前窗口句柄
   # allHandle = browser.window_handles #获取所有句柄
    # all_han = browser.window_handles
    # new_han = [x for x in all_han if x != allHandles][0]
    # print("切换window")
    # browser.switch_to.window(new_han)
    # 获取打开的多个窗口句柄
    allWindows = browser.window_handles
    # 切换到当前最新打开的窗口
    print(allWindows)
    print("切换到新窗口")
    print(allWindows[-1])
    chatWindowHandle = allWindows[-1]
    browser.switch_to.window(chatWindowHandle)
    print("当前窗口是")
    print(browser.current_window_handle)

def reEnterPassword():
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#ap_password")))
    passwdInput = browser.find_element_by_id("ap_password")
    passwdInput.send_keys("aK642u925")
    print("inputing passwd")
    # 勾选rememberme
    remeberMe = browser.find_element_by_css_selector("[name='rememberMe']")
    remeberMe.click()
    print("check remeberme")
    # 确认登录
    submitBtn = browser.find_element_by_id("auth-signin-button")
    submitBtn.click()
    print("confirm login")


def talkToBot():

    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".smartcs-buttons-button")))
    chat1=browser.find_elements_by_css_selector(".smartcs-buttons-button")

    chat1 = chat1[-1]
    chat1.click()
    chat2 = browser.find_elements_by_css_selector(".smartcs-buttons-button")[-1]
    chat2.click()
    textArea=browser.find_element_by_css_selector(".textarea-input")
    textArea.send_keys("Hi")

    #发送
    #browser.find_element_by_xpath("//span[text()='Send message']").click()


def closeChatWindows():
    #关闭所有非起始窗口的所有窗口

    all_handles = browser.window_handles

    for handle in all_handles:
        if handle != mainWindowHandle:
            browser.switch_to.window(handle)
            browser.close()


def mainChat(good_url):


    #STEP 1 打开商品页面
    openGoodsProfile(good_url)
    #STEP 2 检测是否三方卖家并获取商家按钮
    sellerBtn = getSellerBtn()

    if not sellerBtn:
        return False
    else:
        #STEP 3 打开商家详情页
        openSellerProfile(sellerBtn)
        #STEP 4 切换至新打开的页面
        switch_window()
        #此时有可能会出现要求输入密码登录界面，需要处理
        try:
            reEnterPassword()
        except Exception as e:
            print("没有弹出输入密码界面")
            print(e)
        finally:
            talkToBot()


if __name__ == '__main__':
    workbook = xlrd.open_workbook('./goodsList/foot mask.xls')
    # 根据sheet索引或者名称获取sheet内容
    sheet1 = workbook.sheet_by_index(0)  # sheet索引从0开始
    # sheet1 = workbook.sheet_by_name('sheet2')
    # sheet1的名称，行数，列数
    # 获取整行和整列的值（数组）
    cols = sheet1.col_values(5)  # 获取第1列内容
    openMainPageWithCookie('./utils/amazonck.txt')
    mainWindowHandle = browser.current_window_handle  # 获取当前窗口句柄
    count = 0
    for url in cols:
        try:
            good_url="https://www.amazon.co.uk/{0}".format(url)
            mainChat(good_url)
            count += 1
            print("已经处理{}".format(count))
        except Exception as e:
            print(e)
            continue
        closeChatWindows()
        browser.switch_to.window(mainWindowHandle)


