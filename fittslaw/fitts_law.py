# Stellt die Komponenten für die grafische Benutzeroberfläche bereit.
import tkinter as tk


# Platzhalteransicht für die spätere Fitts-Law-Aufgabe.
class FittsLaw(tk.Frame):
    """Zeigt den aktuellen Entwicklungsstand der Fitts-Law-Aufgabe."""

    def __init__(self, parent, app):
        """Erstellt Überschrift, Platzhaltertext und Navigation."""
        # Initialisiert den Frame innerhalb des übergebenen Elternelements.
        super().__init__(parent)

        # Zeigt die Überschrift der Aufgabe an.
        tk.Label(self, text="Fitts' Law Aufgabe", font=("Arial", 24)).pack(pady=20)

        # Kennzeichnet den Bereich, in dem die Aufgabe später eingefügt wird.
        tk.Label(
            self,
            text="Hier kommt später die Fitts' Law Aufgabe hin."
        ).pack(pady=20)

        # Ermöglicht die Rückkehr zum Hauptmenü.
        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=20)
