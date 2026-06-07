import math
import random

from .animation import Animation


class Folgebewegung(Animation):
    """Simuliert eine gleichmäßige Smooth-Pursuit-Augenbewegung."""

    def __init__(self, canvas):
        super().__init__(canvas)
        self.radius = 18
        self.speed = 3

        # Aktuelle Position des Punkts.
        self.x = 0
        self.y = 0

        # Aktueller Endpunkt der Bewegung.
        self.end_x = 0
        self.end_y = 0

        # Gegenüberliegender Endpunkt für die anschließende Rückbewegung.
        self.opposite_x = 0
        self.opposite_y = 0

        # Canvas-ID des gezeichneten Zielpunkts.
        self.target = None

        # Lesbare Bezeichnung der zufällig gewählten Strecke.
        self.route_name = ""

    def setup(self):
        """Wählt zufällig eine Strecke und erstellt den roten Zielpunkt."""
        # Ermittelt die aktuell verfügbare Größe der Zeichenfläche.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Legt die erreichbaren Grenzen so fest, dass der Punkt sichtbar bleibt.
        left = self.radius
        right = max(self.radius, width - self.radius)
        top = self.radius
        bottom = max(self.radius, height - self.radius)

        # Berechnet den Mittelpunkt für horizontale und vertikale Strecken.
        center_x = width / 2
        center_y = height / 2

        # Jede Strecke ist zweimal enthalten, jeweils mit anderer Startrichtung.
        routes = [
            ("links nach rechts", (left, center_y), (right, center_y)),
            ("rechts nach links", (right, center_y), (left, center_y)),
            ("oben nach unten", (center_x, top), (center_x, bottom)),
            ("unten nach oben", (center_x, bottom), (center_x, top)),
            ("oben links nach unten rechts", (left, top), (right, bottom)),
            ("unten rechts nach oben links", (right, bottom), (left, top)),
            ("oben rechts nach unten links", (right, top), (left, bottom)),
            ("unten links nach oben rechts", (left, bottom), (right, top)),
        ]

        # Übernimmt Name, Startpunkt und Endpunkt einer zufälligen Strecke.
        self.route_name, start, end = random.choice(routes)

        # Setzt die aktuelle Position auf den gewählten Startpunkt.
        self.x, self.y = start

        # Speichert den ersten Zielpunkt der Bewegung.
        self.end_x, self.end_y = end

        # Bewahrt den Startpunkt als Ziel für die spätere Rückbewegung auf.
        self.opposite_x, self.opposite_y = start

        # Zeichnet den roten Zielpunkt an seiner Startposition.
        self.target = self.canvas.create_oval(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius,
            fill="red",
            outline=""
        )

    def animate(self):
        """Bewegt den Zielpunkt gleichmäßig entlang der gewählten Strecke."""
        # Bricht ab, wenn die Animation gestoppt wurde oder kein Ziel existiert.
        if self.target is None:
            return

        # Berechnet den Richtungsvektor vom aktuellen zum nächsten Endpunkt.
        distance_x = self.end_x - self.x
        distance_y = self.end_y - self.y

        # Bestimmt die euklidische Restdistanz zum Endpunkt.
        distance = math.hypot(distance_x, distance_y)

        if distance <= self.speed:
            # Ziel exakt erreichen und anschließend zurückbewegen.
            self.x, self.y = self.end_x, self.end_y
            self.end_x, self.end_y, self.opposite_x, self.opposite_y = (
                self.opposite_x,
                self.opposite_y,
                self.end_x,
                self.end_y,
            )
        elif distance > 0:
            # Normierter Vektor sorgt in jeder Richtung für dieselbe Geschwindigkeit.
            self.x += self.speed * distance_x / distance
            self.y += self.speed * distance_y / distance

        # Aktualisiert die Begrenzungskoordinaten des Zielpunkts auf dem Canvas.
        self.canvas.coords(
            self.target,
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )

        # Etwa 60 Bilder pro Sekunde sorgen für eine flüssige Bewegung.
        self.after_id = self.canvas.after(16, self.animate)
