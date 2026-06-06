import tkinter as tk


class AugenBewegung(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        main_frame = tk.Frame(self)
        main_frame.pack(anchor="center")

        tk.Label(
            main_frame,
            text="Augenbewegungen",
            font=("Arial", 24)
        ).pack(pady=20)

        self.canvas = tk.Canvas(
            main_frame,
            width=1400,
            height=700,
            bg="white"
        )
        self.canvas.pack()

        controls_frame = tk.Frame(main_frame)
        controls_frame.pack(pady=20)

        button_frame = tk.Frame(controls_frame)
        button_frame.pack()

        tk.Button(
            button_frame,
            text="Sakkaden"
        ).pack(side="left", padx=20)

        tk.Button(
            button_frame,
            text="Vergenzbewegung"
        ).pack(side="left", padx=20)

        tk.Button(
            button_frame,
            text="Smooth Pursuit"
        ).pack(side="left", padx=20)

        tk.Button(
            controls_frame,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=15)