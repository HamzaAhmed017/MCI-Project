# Stellt die Komponenten für die grafische Benutzeroberfläche bereit.
import tkinter as tk


# Platzhalteransicht für die spätere Auswertung.
class Analyse(tk.Frame):
    """Zeigt den aktuellen Entwicklungsstand der Datenauswertung."""

    def __init__(self, parent, app):
        """Erstellt Überschrift, Platzhaltertext und Navigation."""
        # Initialisiert den Frame innerhalb des übergebenen Elternelements.
        super().__init__(parent)

        # Zeigt die Überschrift der Auswertungsansicht an.
        tk.Label(self, text="Auswertung", font=("Arial", 24)).pack(pady=20)

        # Kennzeichnet den Bereich, in dem später der Scatterplot erscheint.
        tk.Label(
            self,
            text="Hier kommt später der Scatterplot hin."
        ).pack(pady=20)

        # Ermöglicht die Rückkehr zum Hauptmenü.
        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=20)
