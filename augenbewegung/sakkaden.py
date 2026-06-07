import random
from .animation import Animation


# Animation eines Blickpunkts, der sprunghaft seine Position wechselt.
class Sakkaden(Animation):

    def __init__(self, canvas):
        """Initialisiert Größe und Canvas-ID des Blickpunkts."""
        super().__init__(canvas)
        self.radius = 15
        self.point = None

    def setup(self):
        """Erstellt den Blickpunkt zu Beginn der Animation."""
        self.point = self.canvas.create_oval(
            100,
            100,
            100 + 2 * self.radius,
            100 + 2 * self.radius,
            fill="black"
        )

    def animate(self):
        """Verschiebt den Blickpunkt und plant die nächste Sakkade."""
        # Bricht ab, wenn die Animation gestoppt wurde oder kein Punkt existiert.
        if self.point is None:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Tkinter kann vor dem vollständigen Aufbau noch Größe 1 melden.
        if width < 2 * self.radius or height < 2 * self.radius:
            self.after_id = self.canvas.after(50, self.animate)
            return

        # Wählt eine zufällige Position, an der der Punkt vollständig sichtbar ist.
        x = random.randint(self.radius, width - self.radius)
        y = random.randint(self.radius, height - self.radius)

        # Verschiebt den Punkt unmittelbar an die neue Position.
        self.canvas.coords(
            self.point,
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius
        )

        # Wählt eine realistische Pause bis zum nächsten Blicksprung.
        delay = random.randint(800, 1100)

        # Plant den nächsten Animationsschritt und speichert dessen Tkinter-ID.
        self.after_id = self.canvas.after(delay, self.animate)
