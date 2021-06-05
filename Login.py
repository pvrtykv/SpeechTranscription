import binascii
import hashlib
import os
import tkinter as tk
from utils import *

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Login Site", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        button1.pack()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, text="Username * ").pack()
        self.username_login_entry = tk.Entry(self, textvariable=self.username)
        self.username_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Label(self, text="Password * ").pack()
        self.password_login_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_login_entry.pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Login", width=10, height=1, command=self.login_verify).pack()
        self.focus_set()
        self.bind(self, '<Return>', (lambda event: self.login_verify()))

    def login_verify(self, event=None):
        username1 = self.username.get()
        password1 = self.password.get()
        self.username_login_entry.delete(0, 'end')
        self.password_login_entry.delete(0, 'end')

        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            password = verify[1]

            if self.verify_password(password, password1):
                self.login_success()

            else:
                self.password_not_recognised()

        else:
            self.user_not_found()

    def login_success(self):

        self.controller.show_frame("MainPage")

    def password_not_recognised(self):

        password_not_recog_screen = tk.Toplevel(self)
        password_not_recog_screen.title("Success")
        password_not_recog_screen.geometry("150x100")
        tk.Label(password_not_recog_screen, text="Invalid Password ").pack()
        tk.Button(password_not_recog_screen, text="OK",
                  command=password_not_recog_screen.destroy).pack()

    def user_not_found(self):

        user_not_found_screen = tk.Toplevel(self)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100")
        tk.Label(user_not_found_screen, text="User Not Found").pack()
        tk.Button(user_not_found_screen, text="OK", command=user_not_found_screen.destroy).pack()

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

