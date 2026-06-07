import tkinter as tk

class ShortMemory(tk.Frame):
    """Verwaltet die Oberfläche und Steuerung der Kurzzeitgedächtnis test."""
    def __init__(self, master, app):
        tk.Frame.__init__(self, master)

        main_frame = tk.Frame(self)
        main_frame.pack(anchor="center")

        tk.Label(
            main_frame,
            text="Augenbewegungen",
            font=("Arial", 24)
        ).pack(pady=20)
        
        tk.Button(
            self,
            text="Zurück zum Menü",
            command=app.show_main_menu
        ).pack(pady=15)