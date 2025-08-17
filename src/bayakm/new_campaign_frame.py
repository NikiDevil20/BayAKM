import customtkinter as ctk


class NewCampaignFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)

        for row in range(6):
            self.rowconfigure(row, weight=1)
        for col in range(6):
            self.columnconfigure(col, weight=1)

        self._create_widget_frame()
        self._create_widgets()
        self._create_setup_parameters_frame()
        self._create_get_recommendation_frame()

    def _create_widget_frame(self):
        self.widget_frame = ctk.CTkFrame(
            master=self,
            fg_color="dark grey"
        )

        for row in range(6):
            self.widget_frame.rowconfigure(row, weight=1)
        for col in range(6):
            self.widget_frame.columnconfigure(col, weight=1)
        self.widget_frame.grid(row=0, column=0, pady=10, padx=30)
        label = ctk.CTkLabel(master=self.widget_frame, text="Step 1:", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=6, pady=2, padx=10)

    def _create_widgets(self):
        widget_config = (
            ("Choose acquisition function", ctk.CTkOptionMenu, None, {"values": ("qLogEI", "UCB", "qPI")}),
            ("Batchsize", ctk.CTkEntry, 1, {}),
            ("Show probability of improvement", ctk.CTkCheckBox, True, {})
        )
        for i, (widget_name, widget_type, widget_default, widget_kwargs) in enumerate(widget_config):
            label = ctk.CTkLabel(
                master=self.widget_frame,
                text=widget_name,
                text_color="black",
                width=150
            )
            widget = widget_type(
                master=self.widget_frame,
                **widget_kwargs,
                text_color="black",
                width=150
            )
            if isinstance(widget, ctk.CTkEntry):
                widget.insert(0, widget_default)
            if isinstance(widget, ctk.CTkCheckBox):
                widget.configure(
                    text=""
                )
                if widget_default:
                    widget.select()
                else:
                    widget.deselect()
            if isinstance(widget, ctk.CTkOptionMenu):
                widget.set(widget_default)
            label.grid(row=i+1, column=0, pady=2, padx=10)
            widget.grid(row=i+1, column=1, pady=2, padx=10)

    def _create_setup_parameters_frame(self):
        self.get_recommendation_frame = ctk.CTkFrame(
            master=self,
            fg_color="dark grey"
        )
        label = ctk.CTkLabel(master=self.get_recommendation_frame, text="Step 2:", font=("Arial", 24))
        label.pack(pady=2)
        button = ctk.CTkButton(
            master=self.get_recommendation_frame,
            text="Setup parameters",
            text_color="black",
            height=30,
            command=lambda: self._setup_parameters()
        )
        button.pack(pady=2)
        self.get_recommendation_frame.grid(row=1, column=0, pady=10, padx=30, sticky="ew")

    def _setup_parameters(self):
        subwindow = ctk.CTkToplevel(self)
        subwindow.title("Setup parameters")
        subwindow.grab_set()
        subwindow.focus_set()
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        subwindow.frame = ctk.CTkFrame(master=subwindow)
        subwindow.frame.grid(row=0, column=0, sticky="nsew")
        label = ctk.CTkLabel(master=subwindow.frame, text="Text")
        label.pack()

    def _create_get_recommendation_frame(self):
        self.get_recommendation_frame = ctk.CTkFrame(
            master=self,
            fg_color="dark grey"
        )
        label = ctk.CTkLabel(master=self.get_recommendation_frame, text="Step 3:", font=("Arial", 24))
        label.pack(pady=2)
        button = ctk.CTkButton(
            master=self.get_recommendation_frame,
            text="Get recommendation",
            text_color="black",
            height=30,
            command=lambda: self._get_recommendation()
        )
        button.pack(pady=2)
        self.get_recommendation_frame.grid(row=2, column=0, pady=10, padx=30, sticky="ew")

    def _get_recommendation(self):
        pass
