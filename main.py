from selenium import webdriver  # 导入库
import ChatBot
import requests

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_driver = r"chromedriver.exe"


bot = ChatBot(chrome_driver,chrome_options)