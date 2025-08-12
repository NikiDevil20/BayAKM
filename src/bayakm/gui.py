import customtkinter as ctk
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.initialize_geometry()
        self.main_frame()

    def initialize_geometry(self):
        self.title("BayAKM")

    def main_frame(self):
        main_frame = ctk.CTkFrame(
            master=self,
            fg_color="grey",
            corner_radius=10,
            width=800,
            height=600,
        )
        for row in range(3):
            main_frame.rowconfigure(row, weight=0)
        for column in range(3):
            main_frame.columnconfigure(column, weight=0)
        main_frame.pack(

        )


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
