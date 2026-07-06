import tkinter as tk

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