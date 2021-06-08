from tkinter import font as tkfont  # python 3
import tkinter.ttk as ttk
from Login import *
from MainPage import *
from Register import *

app = None

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconphoto(True, tk.PhotoImage(file='images/icon.png'))
        self.title('Speech Transcription')
        self.title_font = tkfont.Font(family='Helvetica', size=18)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        position_right = int(self.winfo_screenwidth() / 2 - self.winfo_reqwidth() / 2)
        position_down = int(self.winfo_screenheight() / 2 - self.winfo_reqheight() / 2)

        self.geometry("+{}+{}".format(position_right, position_down))

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


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Welcome", font=controller.title_font, anchor=tk.CENTER)
        label.pack(side="top", fill="x", pady=10)

        login_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame("Login"))
        register_button = ttk.Button(self, text="Register", command=lambda: controller.show_frame("Register"))
        login_button.pack()
        register_button.pack()


if __name__ == "__main__":
    if not os.path.exists('key.key'):
        write_key()
    app = SampleApp()
    app.mainloop()
