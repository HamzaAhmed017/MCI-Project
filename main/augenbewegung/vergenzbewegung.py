import time
from .animation import Animation


class Vergenzbewegung(Animation):
    """Simuliert abwechselnd Konvergenz und Divergenz der Augen."""

    def setup(self):
        """Initialisiert Positionen und erstellt die beiden Augenpunkte."""
        self.radius = 18
        self.step = 4

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.center_y = height // 2

        # Legt die äußeren Startpositionen links und rechts der Mitte fest.
        self.left_x = width // 2 - 250
        self.right_x = width // 2 + 250

        # Speichert die äußeren Grenzen für die Divergenzbewegung.
        self.outer_left_x = self.left_x
        self.outer_right_x = self.right_x

        # Legt die inneren Grenzen für die Konvergenzbewegung fest.
        self.inner_left_x = width // 2 - 70
        self.inner_right_x = width // 2 + 70

        # Startet mit einer Bewegung beider Punkte zur Mitte.
        self.moving_inward = True

        # Speichert den Startzeitpunkt der aktuellen Bewegungsphase. Ist wichtig, da später die Zeit überprüft wird um
        # Divergenz zu starten
        self.phase_started_at = time.monotonic()

        self.left_eye = self.canvas.create_oval(
            self.left_x - self.radius,
            self.center_y - self.radius,
            self.left_x + self.radius,
            self.center_y + self.radius,
            fill="blue"
        )

        self.right_eye = self.canvas.create_oval(
            self.right_x - self.radius,
            self.center_y - self.radius,
            self.right_x + self.radius,
            self.center_y + self.radius,
            fill="blue"
        )

    def animate(self):
        """Bewegt die Punkte und wechselt regelmäßig die Bewegungsrichtung."""

        # Nach zwei Sekunden zwischen Konvergenz und Divergenz wechseln.
        if time.monotonic() - self.phase_started_at >= 2:
            self.moving_inward = not self.moving_inward
            self.phase_started_at = time.monotonic()

        # Bewegt beide Punkte zur Mitte, ohne die inneren Grenzen zu überschreiten.
        if self.moving_inward:
            self.left_x = min(self.left_x + self.step, self.inner_left_x)
            self.right_x = max(self.right_x - self.step, self.inner_right_x)
        else:
            # Bewegt beide Punkte nach außen bis zu ihren Startpositionen.
            self.left_x = max(self.left_x - self.step, self.outer_left_x)
            self.right_x = min(self.right_x + self.step, self.outer_right_x)

        # Aktualisiert die Position des linken Augenpunkts.
        self.canvas.coords(
            self.left_eye,
            self.left_x - self.radius,
            self.center_y - self.radius,
            self.left_x + self.radius,
            self.center_y + self.radius
        )

        # Aktualisiert die Position des rechten Augenpunkts.
        self.canvas.coords(
            self.right_eye,
            self.right_x - self.radius,
            self.center_y - self.radius,
            self.right_x + self.radius,
            self.center_y + self.radius
        )

        # Plant den nächsten Schritt nach 30 Millisekunden.
        self.after_id = self.canvas.after(30, self.animate)
