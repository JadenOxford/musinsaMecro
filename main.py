import tkinter as tk
import time
from ui import LoginUI
from mecrobot import MusinsaBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class App:
    def __init__(self):
        self.root = tk.Tk()

        # selenium bot
        self.bot = MusinsaBot()

        # UI 생성 + callback 연결
        self.ui = LoginUI(self.root, self.handle_login)

        self.root.mainloop()

    # ================= LOGIN FLOW =================
    def handle_login(self, login_type, user_id, user_pw):
        self.bot.go_login_page() 

        if login_type == "musinsa":
            self.bot.driver.find_element(By.ID, "id").send_keys(user_id)
            # self.bot.driver.find_element(By.ID, "pw").send_keys(password)
            # self.bot.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        elif login_type == "kakao":
            kakao_btn = self.bot.driver.find_element(By.XPATH,"//a[contains(., '카카오로 시작하기')]")
            self.bot.driver.execute_script("arguments[0].click();", kakao_btn)

            WebDriverWait(self.bot.driver, 10).until(EC.presence_of_element_located((By.NAME, "loginId")))

            self.bot.driver.find_element(By.NAME, "loginId").send_keys(user_id)
            self.bot.driver.find_element(By.NAME, "password").send_keys(user_pw)
            self.bot.driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()
            

        elif login_type == "apple":
            self.bot.driver.find_element(By.XPATH, "//a[contains(text(),'Apple로 시작하기')]").click()
        

    # ================= LOGIN FLOW =================

if __name__ == "__main__":
    App()
