import tkinter as tk


class MainMenu(tk.Frame):
    def __init__(self, app):
        super().__init__(app)

        tk.Label(self, text="MCI Projekt", font=("Arial", 24)).pack(pady=30)

        tk.Button(
            self,
            text="Augenbewegungen",
            width=30,
            command=app.show_eye_movement_screen
        ).pack(pady=10)

        tk.Button(
            self,
            text="Fitts' Law",
            width=30,
            command=app.show_fitts_law_screen
        ).pack(pady=10)

        tk.Button(
            self,
            text="Auswertung",
            width=30,
            command=app.show_analysis_screen
        ).pack(pady=10)