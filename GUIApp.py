import binascii
import hashlib
import re
import subprocess
import threading
import time
import tkinter as tk  # python 3
import wave
from tkinter import font as tkfont  # python 3
import os
import utils
from tkinter import filedialog as fd, HORIZONTAL
from tkinter.scrolledtext import ScrolledText
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import pyaudio
import sounddevice as sd
import pygame

app = None


class RecordControl():
    def __init__(self):
        self.finished = False

    def record_audio(self, filename: str):
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 16000

        p = pyaudio.PyAudio()

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []

        while not self.finished:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Login, Register, MainPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Witaj", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Login",
                            command=lambda: controller.show_frame("Login"))
        button2 = tk.Button(self, text="Register",
                            command=lambda: controller.show_frame("Register"))
        button1.pack()
        button2.pack()


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

    def login_verify(self):
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
                  command=lambda: self.delete_screen(password_not_recog_screen)).pack()

    def user_not_found(self):

        user_not_found_screen = tk.Toplevel(self)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100")
        tk.Label(user_not_found_screen, text="User Not Found").pack()
        tk.Button(user_not_found_screen, text="OK", command=lambda: self.delete_screen(user_not_found_screen)).pack()

    def delete_screen(self, screen):
        screen.destroy()

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Register site", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(self, text="Please enter details below", bg="blue").pack()
        tk.Label(self, text="").pack()
        username_label = tk.Label(self, text="Username * ")
        username_label.pack()
        self.username_entry = tk.Entry(self, textvariable=self.username)
        self.username_entry.pack()
        password_label = tk.Label(self, text="Password * ")
        password_label.pack()
        self.password_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self, text="").pack()
        tk.Button(self, text="Register", width=10, height=1, bg="blue", command=self.register_user).pack()

        button = tk.Button(self, text="Go to the start page",
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
        # ----------------


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.is_paused = False
        self.is_playing = False
        self.is_started = False
        self.cwd = os.getcwd()
        self.filetypes = [('text files', '.txt')]
        label = tk.Label(self, text="this is main page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Log out",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        button_recorder = tk.Button(self, text="Record", command=self.record)
        button_recorder.pack()
        button_player = tk.Button(self, text="Play", command=self.play)
        button_player.pack()
        button_reader = tk.Button(self, text="Open text file", command=self.open_file)
        button_reader.pack()
        button_transcribe = tk.Button(self, text="Transcribe", command=self.transcribe_start)
        button_transcribe.pack()

    def record(self):
        record_screen = tk.Toplevel(self)
        record_screen.title("Success")
        record_screen.geometry("150x100")
        tk.Label(record_screen, text="Recording in progress").pack()

        if not os.path.exists('media'):
            os.mkdir('media')
        record_control = RecordControl()
        recording = utils.increment_filename("media/recording.wav")
        thread = threading.Thread(target=record_control.record_audio, args=(recording,))
        thread.start()
        tk.Button(record_screen, text="STOP",
                  command=lambda: self.delete_screen(record_screen, record_control, thread)).pack()

    def play(self):
        audio = fd.askopenfilename(title="Open wav file", initialdir=self.cwd + '/media')
        if audio:
            play_screen = tk.Toplevel(self)
            play_screen.title("Play")
            play_screen.geometry("200x200")

            pygame.mixer.init()
            pygame.mixer.music.load(audio)

            controls_frame = tk.Frame(play_screen)
            controls_frame.grid(pady=20)

            play_btn_img = tk.PhotoImage(file="images/play.png")
            pause_btn_img = tk.PhotoImage(file="images/pause.png")
            stop_btn_img = tk.PhotoImage(file="images/stop.png")

            play_btn = tk.Button(controls_frame, image=play_btn_img, command=self.play_audio)
            play_btn.image = play_btn_img
            pause_btn = tk.Button(controls_frame, image=pause_btn_img, command=self.pause)
            pause_btn.image = pause_btn_img
            stop_btn = tk.Button(controls_frame, image=stop_btn_img, command=self.stop)
            stop_btn.image = stop_btn_img

            play_btn.grid(row=0, column=0, padx=10)
            pause_btn.grid(row=0, column=1, padx=10)
            stop_btn.grid(row=0, column=2, padx=10)

    def play_audio(self):
        if self.is_playing is False:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.is_playing = True
            else:
                pygame.mixer.music.play()
                time.sleep(2)
                self.is_playing = True

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_started = False

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            time.sleep(2)
            self.is_paused = True

    def delete_screen(self, screen, record_control, thread):
        record_control.finished = True
        thread.join()
        screen.destroy()

    def delete_screen(self, screen):
        screen.destroy()

    def open_file(self):
        file = fd.askopenfilename(title="Open text file", initialdir=self.cwd, filetypes=self.filetypes)
        if file:
            file_screen = tk.Toplevel(self)
            text = ScrolledText(file_screen, height=30, width=30)

            with open(file, 'r') as f:
                text.insert(tk.END, f.read())
            text.pack()
            tk.Button(file_screen, text="STOP", command=lambda: self.delete_screen(file_screen)).pack()

    def transcribe_start(self):
        file = fd.askopenfilename(title="Open wav file", initialdir=self.cwd + '/media')

        def run():
            print("job started")
            text = self.transcribe(file)
            self.delete_screen(progress_screen)
            app.after(0, self.transcribe_finish, text)

        def on_closing():
            pass

        thread = threading.Thread(target=run)
        thread.setDaemon(True)
        thread.start()

        progress_screen = tk.Toplevel(self)
        progress_screen.title("Transcription in progress")
        progress_screen.geometry('350x100')
        progress_screen.grab_set()  # zablokowanie głównego okna
        progress_screen.protocol("WM_DELETE_WINDOW", on_closing)

        progress_bar = tk.ttk.Progressbar(progress_screen, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        progress_bar.pack(expand=True)
        progress_bar.start()

    def transcribe_finish(self, text):
        print("job done")
        transcribe_screen = tk.Toplevel(self)
        view = ScrolledText(transcribe_screen, height=30, width=30)
        view.insert(tk.END, text)
        view.pack()

    def transcribe(self, file):
        if file:
            file_list = open("julius/test.dbl", 'w')
            file_list.write(file)
            file_list.close()

            if not os.path.exists('julius_output'):
                os.mkdir('julius_output')

            output = utils.increment_filename("julius_output/output.txt")

            subprocess.run(["julius-dnn", "-C", "julius.jconf", "-dnnconf", "dnn.jconf", ">", "../" + output],
                           shell=True, cwd="julius",
                           check=True)

            r = re.compile(r"sentence1: <s> (.+?) </s>")

            f1 = open(output, 'r')
            lines = f1.readlines()
            f1.close()

            if not os.path.exists('transcriptions'):
                os.mkdir('transcriptions')

            transcription = utils.increment_filename("transcriptions/transcription.txt")
            f2 = open(transcription, 'a')

            for line in lines:
                c = r.match(line)
                if c is not None:
                    f2.write("\n")
                    f2.write(c.group(1))

            f2.close()
            with open(transcription, 'r') as f:
                return f.read()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
