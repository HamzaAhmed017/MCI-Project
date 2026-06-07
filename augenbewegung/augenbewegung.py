import tkinter as tk

# Importiert die verfügbaren Arten von Augenbewegungsanimationen.
from .folgebewegung import Folgebewegung
from .sakkaden import Sakkaden
from .vergenzbewegung import Vergenzbewegung


class AugenBewegung(tk.Frame):
    """Verwaltet die Oberfläche und Steuerung der Augenanimationen."""

    def __init__(self, parent, app):
        """Erstellt Canvas, Animationen und zugehörige Bedienelemente."""
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

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)

        animation_buttons = tk.Frame(button_frame)
        animation_buttons.pack()

        self.sakkaden = Sakkaden(self.canvas)
        self.vergenzbewegung = Vergenzbewegung(self.canvas)
        self.folgebewegung = Folgebewegung(self.canvas)

        self.active_animation = None

        # Startet die Sakkadenanimation.
        tk.Button(
            animation_buttons,
            text="Sakkaden",
            command=self.start_sakkaden
        ).pack(side="left", padx=20)

        # Startet die Vergenzanimation.
        tk.Button(
            animation_buttons,
            text="Vergenzbewegung",
            command=self.start_vergenzbewegung
        ).pack(side="left", padx=20)

        # Startet die gleichmäßige Folgebewegung.
        tk.Button(
            animation_buttons,
            text="Smooth Pursuit",
            command=self.start_folgebewegung
        ).pack(side="left", padx=20)

        # Stoppt die aktuell laufende Animation.
        tk.Button(
            animation_buttons,
            text="Animation stoppen",
            command=self.stop_animation
        ).pack(side="left", padx=20)

        # Ermöglicht die Rückkehr zum Hauptmenü.
        tk.Button(
            button_frame,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=15)

    def start_sakkaden(self):
        """Startet die Animation der sakkadischen Blicksprünge."""
        self.start_animation(self.sakkaden)

    def start_vergenzbewegung(self):
        """Startet die Animation der Vergenzbewegung."""
        self.start_animation(self.vergenzbewegung)

    def start_folgebewegung(self):
        """Startet die gleichmäßige Folgebewegung."""
        self.start_animation(self.folgebewegung)

    def start_animation(self, animation):
        """Stoppt die bisherige und startet die übergebene Animation."""
        # Verhindert, dass zwei Animationen gleichzeitig aktiv bleiben.
        if self.active_animation is not None:
            self.active_animation.stop()

        # Speichert und startet die neu ausgewählte Animation.
        self.active_animation = animation
        self.active_animation.start()

    def stop_animation(self):
        """Stoppt die aktuell aktive Animation."""
        # Stoppt nur dann, wenn tatsächlich eine Animation aktiv ist.
        if self.active_animation is not None:
            self.active_animation.stop()

            # Entfernt die Referenz auf die zuvor aktive Animation.
            self.active_animation = None
