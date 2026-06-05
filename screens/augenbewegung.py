import tkinter as tk


class AugenBewegung(tk.Frame):
    def __init__(self, app):
        super().__init__(app)

        tk.Label(self, text="Augenbewegungen", font=("Arial", 24)).pack(pady=20)

        tk.Label(
            self,
            text="Hier kommt später die Augenbewegungsaufgabe hin."
        ).pack(pady=20)

        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=20)