import tkinter as tk

from screens.main_menu import MainMenu
from screens.augenbewegung import AugenBewegung
from screens.fitts_law import FittsLaw
from screens.analyse import Analyse


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MCI Projekt")
        self.geometry("900x700")

        self.show_main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        MainMenu(self).pack(fill="both", expand=True)

    def show_eye_movement_screen(self):
        self.clear_window()
        AugenBewegung(self).pack(fill="both", expand=True)

    def show_fitts_law_screen(self):
        self.clear_window()
        FittsLaw(self).pack(fill="both", expand=True)

    def show_analysis_screen(self):
        self.clear_window()
        Analyse(self).pack(fill="both", expand=True)