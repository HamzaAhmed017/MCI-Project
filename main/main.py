"""Einstiegspunkt der MCI-Anwendung."""

if __package__:
    from .app import App
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from main.app import App


def run():
    """Erstellt das Hauptfenster und startet die Tkinter-Ereignisschleife."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    run()
