import customtkinter as ctk


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
        font=("Arial", 20)
    )
    subwindow.label.pack(
        pady=50, padx=50
    )
