import tkinter as tk
import time
import json
import os
from ui import LoginUI, LoginSuccessUI
from mecrobot import MusinsaBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
from selenium.webdriver.common.keys import Keys
import threading


LOGIN_FILE = "loginInfo.json"

class App:
    def __init__(self):
        self.root = tk.Tk()

        self.root.protocol("WM_DELETE_WINDOW",self.close_all)

        # selenium bot
        self.bot = MusinsaBot()

        login_info = self.load_loginInfo()

        if login_info:
            
            # 저장된 로그인 정보가 있으면 자동 로그인
            self.process(
                login_info["login_type"],
                login_info["user_id"],
                login_info["user_pw"]
            )
        else:
            # 없으면 로그인 UI 표시
            self.ui = LoginUI(self.root, self.process)

        self.root.mainloop()

    def process(self, login_type, user_id, user_pw):
        if self.handle_login(login_type, user_id, user_pw):
            threading.Thread(target=self.watch_apply_page,daemon=True).start()
        
    # ================= LOGIN FLOW =================
    def save_loginInfo(self, login_type, user_id, user_pw):
        data = {"login_type": login_type, "user_id": user_id, "user_pw": user_pw}

        with open(LOGIN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_loginInfo(self):
        if not os.path.exists(LOGIN_FILE):
            return None

        with open(LOGIN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not all([
            data.get("login_type"),
            data.get("user_id"),
            data.get("user_pw")
        ]):
            return None

        return data

    def clear_loginInfo(self):
        if os.path.exists(LOGIN_FILE):
            os.remove(LOGIN_FILE)

    def is_login_success(self):
        try:
            # 로그인 페이지에 있으면 실패
            if "/login" in self.bot.driver.current_url:
                return False

            # 메인 페이지로 돌아왔는지 확인
            if "www.musinsa.com/main/musinsa" in self.bot.driver.current_url:
                return True
            # # 로그인 버튼이 있으면 아직 로그인 안 됨
            # self.bot.driver.find_element(By.CSS_SELECTOR,"a[href*='login']")
            # return False
        except Exception as e:
            print(e)
            # return True
            return False

    def handle_login(self, login_type, user_id, user_pw):
        self.bot.go_login_page()

        if login_type == "musinsa":
            self.bot.driver.find_element(By.ID, "id").send_keys(user_id)
            # self.bot.driver.find_element(By.ID, "pw").send_keys(password)
            # self.bot.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        elif login_type == "kakao":
            if "accounts.kakao.com/login" not in self.bot.driver.current_url:
                kakao_btn = self.bot.driver.find_element(By.XPATH,"//a[contains(., '카카오로 시작하기')]")
                self.bot.driver.execute_script("arguments[0].click();", kakao_btn)

                
        elif login_type == "apple":
            self.bot.driver.find_element(By.XPATH, "//a[contains(text(),'Apple로 시작하기')]").click()

        id_input = self.bot.driver.find_element(By.NAME,"loginId")

        pw_input = self.bot.driver.find_element(By.NAME,"password")

        # 기존 값 제거 시 clear 함수 적용 안됨 이슈로 command + a, control + a 사용
        modifier = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        # 기존 값 제거
        id_input.click()
        id_input.send_keys(modifier, "a")
        id_input.send_keys(Keys.DELETE)

        pw_input.click()
        pw_input.send_keys(modifier, "a")
        pw_input.send_keys(Keys.DELETE)

        # 값 입력
        id_input.send_keys(user_id)
        pw_input.send_keys(user_pw)   
        
        # 로그인
        self.bot.driver.find_element(By.CSS_SELECTOR,"button[type='submit']").click()

        # 로그인 성공/실패 체크
        try:
            WebDriverWait(self.bot.driver, 10).until(lambda d: self.is_login_success())

            # 로그인 정보 json에 저장
            self.save_loginInfo(login_type, user_id, user_pw)
            print("로그인 성공")
            print("driver =", self.bot.driver)
            print("session =", self.bot.driver.session_id)

            # 로그인 유저명 가져오기 
            user_name = self.bot.get_user_name()

            self.bot.go_experience_page()

            # 유저명을 파라미터로 ui 띄우기 
            self.open_success_window(user_name)

            return True
            
        except Exception as e:
            print(e)
            print("로그인 실패")
            return False

    def open_success_window(self, user_name):
        for widget in self.root.winfo_children():
            widget.destroy()

        LoginSuccessUI(self.root, user_name, self.logout)

    def logout(self):
        try:
            logout_btn = self.bot.driver.find_element(By.CSS_SELECTOR,"a[href*='logout']")
            logout_btn.click()

            print("로그아웃 완료")

            # 저장된 로그인 정보 삭제
            self.clear_loginInfo()

            # 현재 Success UI 제거
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # 다시 로그인 화면
            self.ui = LoginUI(
                self.root,
                self.handle_login
            )

        except Exception as e:
            print("로그아웃 실패:", e)
    # ===============================================



    # ================= AUTO 체험단  =================
    def watch_apply_page(self):
        while self.bot.driver is None:
            time.sleep(0.5)

        last_handles = set(self.bot.driver.window_handles)

        while True:
            try:
                current_handles = set(self.bot.driver.window_handles)

                new_handles = current_handles - last_handles
            
                if new_handles:
                    handle = next(iter(new_handles))   # 새 창 하나
                    self.bot.driver.switch_to.window(handle)
                
                     # 상품 상세 페이지에서 신청하기 한 번만 클릭
                    try:
                        select_option_btn = self.bot.driver.find_element(By.XPATH,"//button[contains(., '신청')]")

                        select_option_btn_text = select_option_btn.text.strip()

                        if select_option_btn_text == "신청 완료":
                            print("이미 신청 완료")

                        elif select_option_btn_text == "신청하기":
                            print("신청 가능")
                            self.bot.driver.execute_script("arguments[0].click();",select_option_btn)
                    except Exception as e:
                        print("신청하기 버튼 클릭 실패", e)

                    while True:
                        # 수동으로 창이 닫혔다면 종료
                        if handle not in self.bot.driver.window_handles:
                            print("상품 창이 수동으로 닫힘")
                            last_handles = current_handles
                            break

                        url = self.bot.driver.current_url

                        if url and "preuser/apply/" in url:
                            print("apply 창 감지")
                            self.bot.complete_apply()
                            break

                        time.sleep(1)

                last_handles = current_handles
                
            except Exception as e:
                print(e)
                time.sleep(1)
    # ===============================================

    # ================= 종료 =================
    def close_all(self):
        print("전체 종료")

        # # Selenium Chrome 종료
        # try:
        #     if self.bot.driver:
        #         self.bot.driver.quit()
        #         self.bot.driver = None
        # except Exception as e:
        #     print("Chrome 종료 오류:", e)

        # Tkinter 종료
        try:
            self.root.destroy()
        except Exception as e:
            print("UI 종료 오류:", e)

    # ===============================================

        
if __name__ == "__main__":
    App()
