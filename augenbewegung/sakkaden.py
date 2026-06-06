import random


class Sakkaden:
    """Steuert die zufälligen Sprünge eines Punktes auf einem Canvas."""

    def __init__(self, canvas):
        # Canvas speichern, auf dem die Animation dargestellt wird.
        self.canvas = canvas

        # Gibt an, ob die Animation aktuell läuft.
        self.running = False

    def start(self):
        # Keine zweite Animationsschleife starten, wenn bereits eine läuft.
        if self.running:
            return

        # Größe und Startposition des dargestellten Punktes festlegen.
        self.radius = 15
        self.point = self.canvas.create_oval(
            100, 100, 130, 130,
            fill="black"
        )

        self.running = True
        self.animate()

    def stop(self):
        # Die nächste Ausführung von animate wird sofort beendet.
        self.running = False

    def animate(self):
        # Animation nicht fortsetzen, wenn stop aufgerufen wurde.
        if not self.running:
            return

        # Aktuelle Größe des Canvas abfragen.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Warten, falls das Canvas noch nicht vollständig aufgebaut wurde.
        if width < self.radius * 2 or height < self.radius * 2:
            self.canvas.after(50, self.animate)
            return

        # Eine zufällige Position wählen, an der der Kreis vollständig innerhalb des Canvas bleibt.
        x = random.randint(self.radius, width - self.radius)
        y = random.randint(self.radius, height - self.radius)

        # Den vorhandenen Punkt an die neue Position verschieben.
        self.canvas.coords(
            self.point,
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius
        )

        # Zufällige Wartezeit zwischen 0,8 und 1,1 Sekunden festlegen.
        delay = random.randint(800, 1100)

        # animate nach der Wartezeit erneut durch Tkinter aufrufen lassen.
        self.canvas.after(delay, self.animate)
