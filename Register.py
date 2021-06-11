import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from utils import *


class Register(ttk.Frame):

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

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def register_user(self):
        if not self.user_already_exists() and self.check_password_length() and self.check_username_length():
            if not os.path.exists("users.txt"):
                open("users.txt", "x")
            username_info = self.username.get()
            password_info = self.password.get()
            encrypted_password = hash_password(password_info)

            file = open("users.txt", "a")
            file.write(username_info + "\n")
            file.write(encrypted_password + "\n")
            file.close()

            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')

            self.controller.show_frame("Login")

    def user_already_exists(self):
        username = self.username.get()
        if not username:
            return False
        if os.path.exists("users.txt"):
            with open("users.txt") as f:
                for line in f:
                    if username == line.strip("\n"):
                        messagebox.showwarning(None, "User already exists!")
                        return True
        return False

    def check_username_length(self):
        username = self.username.get()
        if not username:
            messagebox.showwarning(None, "Please enter username!")
            return False
        return True

    def check_password_length(self):
        password = self.password.get()
        if not password:
            messagebox.showwarning(None, "Please enter password!")
            return False
        return True
