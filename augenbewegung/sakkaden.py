import random

from .animation import Animation


class Sakkaden(Animation):
    """Bewegt einen Blickpunkt in zufälligen Sprüngen über das Canvas."""

    def __init__(self, canvas):
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
        if not self.running or self.point is None:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Tkinter kann vor dem vollständigen Aufbau noch Größe 1 melden.
        if width < 2 * self.radius or height < 2 * self.radius:
            self.after_id = self.canvas.after(50, self.animate)
            return

        x = random.randint(self.radius, width - self.radius)
        y = random.randint(self.radius, height - self.radius)

        self.canvas.coords(
            self.point,
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius
        )

        delay = random.randint(800, 1100)
        self.after_id = self.canvas.after(delay, self.animate)
