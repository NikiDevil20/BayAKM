from typing import Callable

from src.gui.menubar.abstract_menu import AbstractMenu
from src.gui.menubar.open_window import open_window


class CustomMenuBar:
    def __init__(self, master):

        file_dict = {
            "New campaign": open_window(
                master=master,
                name="New campaign",
            ),
            "Open campaign": open_window(
                master=master,
                name="Choose campaign",
            ),
        }

        campaign_dict = {
            "Save": master.table_frame.read_table,
            "New recommendation": master.table_frame.get_new_recommendation,
            "break": None,
            "Add row": master.table_frame.add_empty_row
        }

        insight_dict = {
            "Get insights": None
        }

        help_dict = {
            "Help": None,
            "Report bugs": None
        }

        toplevel_dict = {
            "File": file_dict,
            "Campaign": campaign_dict,
            "Insights": insight_dict,
            "Help": help_dict
        }

        self.menu = AbstractMenu(master, toplevel_dict).return_menu()

    def return_menu(self):
        return self.menu

    def recommend_or_save(self, master, recommendation) -> Callable:
        def command():
            master.refresh_content(recommendation=recommendation)
            master.table_frame.read_table
        return command

