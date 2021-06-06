import tkinter as tk
import tkinter.ttk as ttk
from utils import *


class Register(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Register site", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        ttk.Label(self, text="Please enter details below").pack()
        ttk.Label(self, text="").pack()
        username_label = ttk.Label(self, text="Username * ")
        username_label.pack()
        self.username_entry = ttk.Entry(self, textvariable=self.username)
        self.username_entry.pack()
        password_label = ttk.Label(self, text="Password * ")
        password_label.pack()
        self.password_entry = ttk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack()
        ttk.Label(self, text="", anchor=tk.CENTER).pack()
        ttk.Button(self, text="Register", width=10, command=self.register_user).pack()

        button = ttk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def register_user(self):
        username_info = self.username.get()
        password_info = self.password.get()
        encrypt = hash_password(password_info)

        file = open(username_info, "w")
        file.write(username_info + "\n")
        file.write(encrypt)
        file.close()

        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

        self.controller.show_frame("MainPage")
