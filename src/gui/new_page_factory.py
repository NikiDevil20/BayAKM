from abc import ABC, abstractmethod

import customtkinter as ctk

from src.gui.gui_constants import FGCOLOR, HEADER, CONTENTFRAMECOLOR, BOTTOMFRAMECOLOR, TEXTCOLOR, STANDARD


class BaseFrame(ctk.CTkFrame, ABC):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.header: str | None = None
        self.bottomtext: str | None = None
        self.header_frame: ctk.CTkFrame | None = None
        self.content_frame: ctk.CTkFrame | None = None
        self.bottom_frame: ctk.CTkFrame | None = None

    def build_frames(self):
        self.header_frame = self.create_generic_frame(
            fg_color=FGCOLOR,
            row=0,
            column=0
        )

        self.create_generic_label(
            master=self.header_frame,
            text=self.header,
            font=HEADER
        )

        self.content_frame = self.create_generic_frame(
            fg_color=CONTENTFRAMECOLOR,
            row=1,
            column=0
        )

        self.bottom_frame = self.create_generic_frame(
            fg_color=BOTTOMFRAMECOLOR,
            row=2,
            column=0
        )

    def create_generic_frame(self, fg_color, row, column):
        frame = ctk.CTkFrame(
            master=self,
            fg_color=fg_color
        )
        frame.grid(pady=10, padx=20, row=row, column=column, sticky="ew")
        return frame

    @staticmethod
    def create_generic_label(master, text, font):
        label = ctk.CTkLabel(
            master=master,
            text=text,
            font=font,
        )
        label.pack(pady=5, padx=10)
        return label

    @staticmethod
    def create_generic_button(master, command, row=0, column=0, text=None):
        button = ctk.CTkButton(
            master=master,
            text_color=TEXTCOLOR,
            fg_color=FGCOLOR,
            font=STANDARD,
            command=command,
            text=text
        )
        button.grid(row=row, column=column, pady=5, padx=10)
        return button

    @abstractmethod
    def fill_content(self):
        pass
