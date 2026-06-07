# Stellt die Komponenten für die grafische Benutzeroberfläche bereit.
import tkinter as tk


# Startansicht mit Schaltflächen zu allen Bereichen der Anwendung.
class MainMenu(tk.Frame):
    """Zeigt die Hauptnavigation der Anwendung an."""

    def __init__(self, parent, app):
        """Erstellt Überschrift und Navigationsschaltflächen."""
        # Initialisiert den Frame innerhalb des übergebenen Elternelements.
        super().__init__(parent)

        # Zeigt die Überschrift des Projekts an.
        tk.Label(self, text="MCI Projekt", font=("Arial", 24)).pack(pady=50)

        # Öffnet die Ansicht mit den verschiedenen Augenbewegungen.
        tk.Button(
            self,
            text="Augenbewegungen",
            width=30,
            command=app.show_eye_movement_screen
        ).pack(pady=10)

        # Öffnet die Fitts-Law-Aufgabe.
        tk.Button(
            self,
            text="Fitts' Law",
            width=30,
            command=app.show_fitts_law_screen
        ).pack(pady=10)

        # Öffnet die Auswertung der aufgezeichneten Daten.
        tk.Button(
            self,
            text="Auswertung",
            width=30,
            command=app.show_analysis_screen
        ).pack(pady=10)
