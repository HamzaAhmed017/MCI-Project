import tkinter as tk
from .sakkaden import Sakkaden


class AugenBewegung(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        main_frame = tk.Frame(self)
        main_frame.pack(anchor="center")

        #Titel
        tk.Label(
            main_frame,
            text="Augenbewegungen",
            font=("Arial", 24)
        ).pack(pady=20)

        #Hier kommt die Animation
        self.canvas = tk.Canvas(
            main_frame,
            width=1400,
            height=700,
            bg="white"
        )
        self.canvas.pack()

        #Controls abtrennen von der Canvas
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        #Buttons von anmachen der Animationen trennen
        animation_buttons_frame = tk.Frame(button_frame)
        animation_buttons_frame.pack()

        self.sakkaden = Sakkaden(self.canvas)

        tk.Button(
            animation_buttons_frame,
            text="Sakkaden",
            command=self.start_sakkaden
        ).pack(side="left", padx=20)

        tk.Button(
            animation_buttons_frame,
            text="Vergenzbewegung"
        ).pack(side="left", padx=20)

        tk.Button(
            animation_buttons_frame,
            text="Smooth Pursuit"
        ).pack(side="left", padx=20)

        tk.Button(
            button_frame,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=15)

    def start_sakkaden(self):
        self.sakkaden.start()
