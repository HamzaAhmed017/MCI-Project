import tkinter as tk


class Analyse(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="Auswertung", font=("Arial", 24)).pack(pady=20)

        tk.Label(
            self,
            text="Hier kommt später der Scatterplot hin."
        ).pack(pady=20)

        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=20)