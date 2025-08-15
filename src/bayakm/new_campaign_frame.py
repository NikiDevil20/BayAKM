import customtkinter as ctk

class NewCampaignFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        label = ctk.CTkLabel(master=self, text="New Campaign")
        label.pack()