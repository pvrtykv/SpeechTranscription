import binascii
import hashlib
import os
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox as messagebox

from cryptography.fernet import Fernet


def write_key():
    key = Fernet.generate_key()
    key_filename = "keys/" + Login.USERNAME + "_key.key"
    with open(key_filename, "wb") as key_file:
        key_file.write(key)


def load_key():
    key_filename = "keys/" + Login.USERNAME + "_key.key"
    if os.path.exists(key_filename):
        return open(key_filename, "rb").read()


class Login(tk.Frame):
    USERNAME = ""
    KEY = ""

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Login Site", font=controller.title_font, anchor=tk.CENTER)
        label.pack(side="top", fill="x", pady=10)
        self.position_right = int(self.winfo_screenwidth() / 2 - self.winfo_reqwidth() / 2)
        self.position_down = int(self.winfo_screenheight() / 2 - self.winfo_reqheight() / 2)
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        ttk.Label(self, text="Username * ").pack()
        self.username_login_entry = ttk.Entry(self, textvariable=self.username)
        self.username_login_entry.pack()
        ttk.Label(self, text="Password * ").pack()
        self.password_login_entry = ttk.Entry(self, textvariable=self.password, show='*')
        self.password_login_entry.pack()
        ttk.Label(self, text="").pack()
        ttk.Button(self, text="Login", command=self.login_verify).pack()
        self.focus_set()
        self.bind(self, '<Return>', (lambda event: self.login_verify()))
        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame("StartPage"))
        button1.pack()

    def login_verify(self, event=None):
        username1 = self.username.get()
        password1 = self.password.get()
        Login.USERNAME = username1
        self.username_login_entry.delete(0, 'end')
        self.password_login_entry.delete(0, 'end')

        if os.path.exists("users.txt"):
            encrypted_password = ""
            username = ""
            with open("users.txt") as f:
                for line in f:
                    next_line = next(f)
                    if username1 == line.strip("\n"):
                        username = line.strip("\n")
                        encrypted_password = next_line.strip("\n")
                        break
            if username:
                if self.verify_password(encrypted_password, password1):
                    self.login_success()
                else:
                    messagebox.showwarning(None, "Wrong password!")
            else:
                messagebox.showwarning(None, "User not found!")

        else:
            messagebox.showwarning(None, "User not found!")

    def login_success(self):
        if not os.path.exists("keys/" + Login.USERNAME + "_key.key"):
            write_key()
        Login.KEY = load_key()
        self.controller.show_frame("MainPage")

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

