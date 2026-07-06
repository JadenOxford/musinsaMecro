from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class MusinsaBot:
    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.driver = None

    # =========================
    # 무신사 로그인 페이지 오픈
    # =========================
    def open_home(self):
        # self.driver = webdriver.Chrome()
        print(1)
        options = webdriver.ChromeOptions()
        print(2)
        options.add_argument(r"--user-data-dir=D:\py\musinsaMecro\chrome_profile")
        print(3)
        self.driver = webdriver.Chrome(options=options)
        print(4)
        self.driver.get("https://www.musinsa.com/main/musinsa")

    def go_login_page(self):
        if self.driver is None:
            self.open_home()
        login_btn = self.driver.find_element(By.CSS_SELECTOR, "a[href*='login']")
        login_btn.click()
        time.sleep(2)