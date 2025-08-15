import customtkinter as ctk

class HelpFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        label = ctk.CTkLabel(master=self, text="Help")
        label.pack()