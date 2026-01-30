import customtkinter as ctk

TEXTCOLOR = "black"
FGCOLOR = "light blue"
BGCOLOR = "light grey"

CONTENTFRAMECOLOR = "light grey"
BOTTOMFRAMECOLOR = "light grey"
ROWFGCOLOR = "grey"

HEADER = ("Inter", 28, "bold")
SUBHEADER = ("Inter", 20)
STANDARD = ("Inter", 14)
SMALL = ("Inter", 10)


class PackagedWidget:
    def __init__(self, widget_type, **kwargs):
        self.widget = None
        self._type = widget_type
        self._kwargs = kwargs

    def configure(self, master):
        self.widget = self._type(master=master, **self._kwargs)
        return self.widget


class Row(ctk.CTkFrame):
    def __init__(self, master, object_list: list[PackagedWidget], weights:list[int]=None):
        ctk.CTkFrame.__init__(self, master)

        if weights is not None and len(object_list) != len(weights):
            raise ValueError("Length of weights must match length of object_list")

        self.object_list = object_list
        self.weights = weights
        self.n_cols = len(object_list)
        self.widget_list = []

        self.display_objects()

    def build_object(self, packaged_widget):
        widget = packaged_widget.configure(master=self)
        return widget

    def display_objects(self):
        for index, packaged_widget in enumerate(self.object_list):
            widget = self.build_object(packaged_widget)
            self.widget_list.append(widget)
            widget.grid(row=0, column=index, sticky="ew", padx=5, pady=2)
            if self.weights is not None:
                self.columnconfigure(index, weight=self.weights[index])
            else:
                self.columnconfigure(index, weight=1)

    def return_widget(self, position: int):
        return self.widget_list[position]



