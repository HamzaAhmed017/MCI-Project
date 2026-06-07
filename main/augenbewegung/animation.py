from abc import ABC, abstractmethod


class Animation(ABC):
    """Definiert Start, Stopp und Rücksetzen einer Animation."""

    def __init__(self, canvas):
        """Speichert das Canvas und initialisiert den Animationszustand."""
        self.canvas = canvas
        self.running = False
        self.after_id = None

    def start(self):
        """Bereitet die Animation vor und startet ihren Ablauf."""
        self.stop()
        self.running = True
        self.canvas.delete("all")
        self.setup()
        self.animate()

    def stop(self):
        """Stoppt die Animation und entfernt einen geplanten Aufruf."""
        self.running = False

        if self.after_id is not None:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        """Stoppt die Animation und leert die Zeichenfläche."""
        self.stop()
        self.canvas.delete("all")

    # Erzwingt eine konkrete Einrichtung in jeder Unterklasse.
    @abstractmethod
    def setup(self):
        """Erstellt die benötigten Elemente der konkreten Animation."""
        pass

    # Erzwingt eine konkrete Bewegungslogik in jeder Unterklasse.
    @abstractmethod
    def animate(self):
        """Führt einen Animationsschritt der konkreten Animation aus."""
        pass
