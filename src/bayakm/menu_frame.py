import customtkinter as ctk


class MainFrame(ctk.CTkFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master)

        for row in range(3):
            self.rowconfigure(row, weight=0)
        for column in range(3):
            self.columnconfigure(column, weight=0)

        # self.configure(
        #     fg_color="grey",
        #     corner_radius=10,
        # )
        self._create_subwindows()

    def _create_subwindows(self):
        btn_config = [
            ("New campaign", lambda: test_func()),
            ("New recommendation", lambda: test_func()),
            ("View Parameters", lambda: test_func()),
            ("Help", lambda: test_func())
        ]
        for i, (text, command) in enumerate(btn_config):
            button = ctk.CTkButton(
                master=self,
                text=text,
                command=command,
                font=("Arial", 18),
                text_color="black",
                height=40,
                width=200,
                fg_color="light blue"
            )
            button.grid(row=i, column=0, pady=5, padx=10)


def test_func():
    print("Test.")


