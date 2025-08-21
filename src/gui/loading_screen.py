import customtkinter as ctk


class LoadingScreen(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title = "Loading..."
        self.geometry("300x150")
        self.update()
        self.grab_set()
        self.focus_set()
        label = ctk.CTkLabel(master=self, text="Loading BayAKM")
        label.pack(expand=True)
