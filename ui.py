import tkinter as tk
from tkinter import ttk


class LoginUI:
    def __init__(self, root, login_callback):
        self.root = root
        self.login_callback = login_callback

        self.root.title("Musinsa Macro")
        self.root.geometry("420x270")
        self.root.resizable(False, False)

        # ================= LOGIN FRAME =================
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.login_frame, text="LOGIN", font=("Arial", 18, "bold")).pack(pady=10)

        # ID
        row1 = tk.Frame(self.login_frame)
        row1.pack(fill="x", pady=5)

        tk.Label(row1, text="계정/이메일", width=10).pack(side="left")
        self.id_entry = tk.Entry(row1)
        self.id_entry.pack(side="left", fill="x", expand=True)

        # PW
        row2 = tk.Frame(self.login_frame)
        row2.pack(fill="x", pady=5)

        tk.Label(row2, text="비밀번호", width=10).pack(side="left")
        self.pw_entry = tk.Entry(row2, show="*")
        self.pw_entry.pack(side="left", fill="x", expand=True)

        # LOGIN TYPE
        group = tk.LabelFrame(self.login_frame, text="로그인 방법", padx=2, pady=2)
        group.pack(fill="x", pady=10)

        self.login_type = tk.StringVar(value="musinsa")

        radio_frame = tk.Frame(group)
        radio_frame.pack(anchor="center")

        tk.Radiobutton(radio_frame, text="무신사", variable=self.login_type, value="musinsa").pack(side="left", padx=25)
        tk.Radiobutton(radio_frame, text="카카오", variable=self.login_type, value="kakao").pack(side="left", padx=25)
        tk.Radiobutton(radio_frame, text="Apple", variable=self.login_type, value="apple").pack(side="left", padx=25)

        # LOGIN BUTTON
        tk.Button(
            self.login_frame,
            text="LOGIN",
            bg="#222",
            fg="white",
            height=2,
            command=self.on_login_click
        ).pack(fill="x", pady=5)

    # ================= UI EVENT =================
    def on_login_click(self):
        self.login_callback(
            self.login_type.get(),
            self.id_entry.get(),
            self.pw_entry.get()
        )

class LoginSuccessUI:

    def __init__(self, root, user_name, logout_callback):

        self.root = root
        self.logout_callback = logout_callback

        self.root.title("Musinsa Macro")
        self.root.geometry("420x300")
        self.root.resizable(False, False)


        # ================= MESSAGE =================
        # 유저명 표시
        tk.Label(root, text=f"{user_name}님", font=("Arial", 13, "bold")
                ).pack(pady=10)

        # 로그아웃 라벨 표시 
        logout = tk.Label(root,text="로그아웃",cursor="hand2",font=("Arial", 9, "underline"))
        logout.pack(pady=10)
        logout.bind("<Button-1>",lambda e: self.logout_callback())

        info = """
함께 띄워지는 Chrome의
무신사 체험단 페이지에서
다음 단계를 진행해주세요.


1. 상품 선택

2. 상품 옵션 선택 및
   선택완료 버튼 클릭


자동으로 신청됩니다.
"""


        tk.Label(
            root,
            text=info,
            justify="left",
            font=("Arial", 11)
        ).pack(
            padx=30,
            anchor="w"
        )
