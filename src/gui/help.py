import customtkinter as ctk

from src.gui.gui_constants import SUBHEADER


class HelpFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        label = ctk.CTkLabel(
            master=self,
            text="Help"
        )
        label.pack()


def error_subwindow(master, message: str):
    subwindow = ctk.CTkToplevel(master)
    subwindow.title("Error")
    subwindow.grab_set()
    subwindow.focus_set()
    subwindow.label = ctk.CTkLabel(
        master=subwindow,
        text=message,
        font=SUBHEADER
    )
    subwindow.label.pack(
        pady=50, padx=50
    )
