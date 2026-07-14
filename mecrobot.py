from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MusinsaBot:
    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.driver = None

    # =========================
    # LOG IN 
    # =========================
    def go_login_page(self):
        if self.driver is None:
            # 무신사 홈
            options = webdriver.ChromeOptions()
            options.add_argument(r"--user-data-dir=D:\py\musinsaMecro\chrome_profile")
            options.add_argument("--profile-directory=Default")

            self.driver = webdriver.Chrome(options=options)
            self.driver.get("https://www.musinsa.com/main/musinsa")

            login_btn = self.driver.find_element(By.CSS_SELECTOR, "a[href*='login']")
            login_btn.click()
            time.sleep(2)

    def get_user_name(self):
        try:
            # current_url = self.driver.current_url

            # 마이페이지 이동
            self.driver.get("https://www.musinsa.com/mypage")

            name_element = WebDriverWait(self.driver,10
            ).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"div.Profile__TextWrapper-sc-9ssgk4-2 a"))
            )

            user_name = name_element.text
            # print(user_name)

            # 마이페이지 나가서 원래 홈페이지로 복귀
            # self.driver.get(current_url)

            return user_name.strip()
        except Exception as e:
            print("사용자 이름 가져오기 실패:", e)
            return "사용자"

    def go_experience_page(self):
        try:
             # 체험단 메뉴 버튼 클릭
            apply_menu = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[contains(text(),'체험단 신청/응모 내역')]]")))

            self.driver.execute_script("arguments[0].click();",apply_menu)

            print("체험단 페이지 이동 완료")

        except Exception as e:
            print("체험단 페이지 이동 실패:", e)


    # =========================
    # 무신사 체험단 페이지에서 수동 옵션 선택 후 자동으로 신청 
    # =========================
    def complete_apply(self):
        driver = self.driver

        # # print("apply 감지 시작")
        # while True:
        #     print(driver.current_url)
        #     time.sleep(1)
        #     try:
        #         # 새 창이 열렸으면 마지막 창으로 이동
        #         if len(driver.window_handles) > 1:
        #             driver.switch_to.window(driver.window_handles[-1])

        #         # 새 창으로 event페이지가 열리고 event페이지에서 선택 완료 를 누르면 apply 페이지가 된다
        #         if "preuser/apply/" in driver.current_url: 
        #             # print("apply 페이지 발견")

        # 전체 동의하기 클릭
        agree = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "all")))
        if agree.get_attribute("aria-checked") == "false": # 체크가 안되어 있을 때에만 체크해라 
            driver.execute_script("arguments[0].click();", agree)

        # print("전체 동의 완료")

        # 신청 완료 버튼 클릭
        apply_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[.//span[contains(., '신청 완료')]]")))
        driver.execute_script("arguments[0].click();", apply_btn)

        # print("신청 완료")

        # 보러가기 버튼이 생길 때까지 기다렸다가 (팝업으로 생성됨) 생기면 클릭
        browse_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(., '보러가기')]")))
        driver.execute_script("arguments[0].click();", browse_btn)

        # print("보러가기 완료")

        # 새창에서 다시 새창이 사라지며 원래 페이지로 돌아가도록 함
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
        driver.switch_to.window(driver.window_handles[0])

        # return;

            # except Exception as e:
            #     print(e)

            # time.sleep(0.2)
    