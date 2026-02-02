import customtkinter as ctk

from src.gui.main.gui_constants import SUBHEADER, FGCOLOR, STANDARD


class HelpTopic(ctk.CTkFrame):
    def __init__(self, master=None, title: str = "", content: str = ""):
        super().__init__(master)

        self.title = title
        self.content = content
        self.state = "collapsed"
        self.text_frame = None
        self.button = None

        self.configure(fg_color=FGCOLOR)

        self._build_header()
        self._build_button()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

    def _build_header(self):
        header = ctk.CTkLabel(
            master=self,
            text=self.title,
            font=SUBHEADER,
        )
        header.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")

    def _build_button(self):
        if self.button:
            self.button.destroy()

        self.button = ctk.CTkButton(
            master=self,
            text="expand" if self.state == "collapsed" else "collapse",
            font=STANDARD,
            command=self._toggle_state,
            width=60,
            height=25
        )
        self.button.grid(row=0, column=1, pady=(10, 5), padx=10)

    def _build_content(self):
        if self.state == "collapsed":
            return

        self.text_frame = ctk.CTkFrame(master=self)
        self.text_frame.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="nsew", columnspan=2)

        label = ctk.CTkLabel(
            master=self.text_frame,
            text=self.content,
            font=STANDARD,
            wraplength=500,
            justify="left"
        )
        label.pack(fill="both", expand=True, pady=10, padx=10)

    def _refresh(self):
        if self.text_frame:
            self.text_frame.destroy()
            self.text_frame = None

        self._build_content()
        self._build_button()

    def _toggle_state(self):
        self.state = "expanded" if self.state == "collapsed" else "collapsed"
        self._refresh()


