import tkinter as tk


class FittsLaw(tk.Frame):
    def __init__(self, app):
        super().__init__(app)

        tk.Label(self, text="Fitts' Law Aufgabe", font=("Arial", 24)).pack(pady=20)

        tk.Label(
            self,
            text="Hier kommt später die Fitts' Law Aufgabe hin."
        ).pack(pady=20)

        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=20)