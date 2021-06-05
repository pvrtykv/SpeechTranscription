import os
import re
import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog as fd
import pygame
from tkinter.scrolledtext import ScrolledText
import utils
from GUIApp import app
from GUIApp import RecordControl
from utils import KEY
import tkinter.ttk as ttk


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


    def delete_screen(self, screen, record_control, thread, recording):
        record_control.finished = True
        thread.join()
        utils.encrypt(recording, KEY)
        screen.destroy()
    '''
    def delete_screen(self, screen, record_control, thread):
        record_control.finished = True
        thread.join()
        screen.destroy()
    '''
    def record(self):
        record_screen = tk.Toplevel(self)
        record_screen.title("Success")
        record_screen.geometry("150x100")
        tk.Label(record_screen, text="Recording in progress").pack()

        if not os.path.exists('media'):
            os.mkdir('media')
        record_control = RecordControl()
        recording = utils.increment_filename("media/ENCrecording.wav")
        thread = threading.Thread(target=record_control.record_audio, args=(recording,))
        thread.start()
        tk.Button(record_screen, text="STOP",
                  command=lambda: self.delete_screen(record_screen, record_control, thread, recording)).pack()

    def play(self):
        audio = fd.askopenfilename(title="Open wav file", initialdir=self.cwd + '/media')
        prefix = os.path.basename(audio)[0:3]
        if audio:
            if prefix == "ENC":
                utils.decrypt(audio, KEY)

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

            def on_closing():
                pygame.mixer.music.unload()
                if prefix == "ENC":
                    utils.encrypt(audio, KEY)

                play_screen.destroy()

            play_screen.protocol("WM_DELETE_WINDOW", on_closing)

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
            self.is_playing = False


    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            # time.sleep(2)
            self.is_paused = True
            self.is_playing = False

    def open_file(self):
        file = fd.askopenfilename(title="Open text file", initialdir=self.cwd, filetypes=self.filetypes)
        prefix = os.path.basename(file)[0:3]
        if file:
            if prefix == "ENC":
                utils.decrypt(file, KEY)
            file_screen = tk.Toplevel(self)
            text = ScrolledText(file_screen, height=30, width=30)

            with open(file, 'r') as f:
                text.insert(tk.END, f.read())
            text.pack()
            if prefix == "ENC":
                utils.encrypt(file, KEY)
            tk.Button(file_screen, text="STOP", command=file_screen.destroy).pack()

    def transcribe_start(self):
        file = fd.askopenfilename(title="Open wav file", initialdir=self.cwd + '/media',
                                  filetypes=[('wav files', '.wav')])

        def run():
            print("job started")
            text = utils.transcribe(file)
            progress_screen.destroy()
            self.transcribe_finish(text)

        def on_closing():
            pass

        if file:
            thread = threading.Thread(target=run)
            thread.setDaemon(True)
            thread.start()

            progress_screen = tk.Toplevel(self)
            progress_screen.title("Transcription in progress")
            progress_screen.geometry('350x100')
            progress_screen.grab_set()  # zablokowanie głównego okna
            progress_screen.protocol("WM_DELETE_WINDOW", on_closing)

            progress_bar = ttk.Progressbar(progress_screen, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
            progress_bar.pack(expand=True)
            progress_bar.start()

    def transcribe_finish(self, text):
        print("job done")
        transcribe_screen = tk.Toplevel(self)
        view = ScrolledText(transcribe_screen, height=30, width=30)
        view.insert(tk.END, text)
        view.pack()

