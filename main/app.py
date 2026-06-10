import tkinter as tk

from .analyse.analyse import Analyse
from .augenbewegung.augenbewegung import AugenBewegung
from .fittslaw.fitts_law import FittsLaw
from .mainmenu.main_menu import MainMenu
from .shortmemory.short_memory import ShortMemory


class App(tk.Tk):
    """Verwaltet das Hauptfenster und die Navigation der Anwendung."""

    def __init__(self):
        """Initialisiert das Fenster, den Kopfbereich und den Inhaltsbereich."""
        super().__init__()

        self.title("MCI Projekt")
        self.attributes("-fullscreen", True)

        self.header = tk.Frame(self)
        self.header.pack(fill="x")

        tk.Button(
            self.header,
            text="Beenden",
            command=self.destroy
        ).pack(side="right", padx=10, pady=10)

        self.content = tk.Frame(self)
        self.content.pack(fill="both", expand=True)

        self.show_main_menu()

    def clear_window(self):
        """Entfernt alle Elemente aus dem Inhaltsbereich."""
        # Durchläuft alle Widgets der aktuell angezeigten Ansicht.
        for widget in self.content.winfo_children():
            # Zerstört das Widget, damit die nächste Ansicht Platz erhält.
            widget.destroy()

    def show_main_menu(self):
        """Wechselt zur Ansicht des Hauptmenüs."""
        self.clear_window()

        MainMenu(self.content, self).pack(fill="both", expand=True)

    def show_eye_movement_screen(self):
        """Wechselt zur Ansicht der Augenbewegungen."""
        self.clear_window()

        AugenBewegung(self.content, self).pack(fill="both", expand=True)

    def show_short_memory_screen(self):
        """Wechselt zur Ansicht dem Kurzzeitgedächtnis."""
        self.clear_window()

        ShortMemory(self.content, self).pack(fill="both", expand=True)

    def show_fitts_law_screen(self):
        """Wechselt zur Ansicht der Fitts-Law-Aufgabe."""
        self.clear_window()

        FittsLaw(self.content, self).pack(fill="both", expand=True)

    def show_analysis_screen(self):
        """Wechselt zur Auswertungsansicht."""
        self.clear_window()

        # Erstellt und zeigt die Analyseansicht.
        Analyse(self.content, self).pack(fill="both", expand=True)
