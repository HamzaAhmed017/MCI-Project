import random
import tkinter as tk

from .short_memory_logic import ShortMemoryTest


class ShortMemory(tk.Frame):
    """Verwaltet die Oberfläche und Steuerung des Kurzzeitgedächtnis-Tests."""

    DISPLAY_MS = 8_000
    BLANK_MS = 8_000

    def __init__(self, master, app):
        """Initialisiert die GUI-Ansicht und zeigt den Startbildschirm an."""
        super().__init__(master)

        self.app = app
        self.mode = tk.StringVar(value="normal")
        self.test = None
        self.after_id = None
        self.current_entries = []

        self._show_start_screen()

    def destroy(self):
        """Beendet laufende Timer, bevor die Tkinter-Ansicht zerstört wird."""
        self._cancel_timer()
        super().destroy()

    def _clear(self):
        """Entfernt alle aktuell angezeigten Widgets aus dieser Ansicht."""
        for widget in self.winfo_children():
            widget.destroy()

    def _cancel_timer(self):
        """Bricht einen geplanten Tkinter-Timer ab, falls einer aktiv ist."""
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def _show_start_screen(self):
        """Zeigt die Startansicht mit Moduswahl und Startknopf an."""
        self._cancel_timer()
        self._clear()

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        tk.Label(
            main_frame,
            text="Kurzzeitgedächtnis-Test",
            font=("Arial", 24)
        ).pack(pady=20)

        tk.Label(
            main_frame,
            text="39 Durchgänge: Längen 3 bis 15, jede Länge 3-mal.",
            font=("Arial", 13)
        ).pack(pady=10)

        button_frame = tk.LabelFrame(main_frame, text="Testversion")
        button_frame.pack(pady=20, padx=20, fill="x")

        tk.Radiobutton(
            button_frame,
            text="Normale Darstellung",
            variable=self.mode,
            value="normal"
        ).pack(anchor="w", padx=15, pady=8)

        tk.Radiobutton(
            button_frame,
            text="Chunkbasiert: 3er-Pakete",
            variable=self.mode,
            value="chunked"
        ).pack(anchor="w", padx=15, pady=8)

        tk.Button(
            main_frame,
            text="Start",
            font=("Arial", 18),
            width=20,
            command=self._start_test
        ).pack(pady=20)

        tk.Button(
            main_frame,
            text="Zurück zum Menü",
            command=self.app.show_main_menu
        ).pack(pady=15)

    def _start_test(self):
        """Erstellt einen neuen Testdurchlauf und startet den ersten Trial."""
        self.test = ShortMemoryTest(self.mode.get())
        self._show_next_sequence()

    def _show_next_sequence(self):
        """Zeigt die nächste zu merkende Zeichenkette für 8 Sekunden an."""
        if not self.test.has_next_trial():
            self._show_plot()
            return

        self.test.next_sequence()
        self._clear()

        frame = tk.Frame(self)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text=f"Durchgang {self.test.trial_number()} von {self.test.total_trials()}",
            font=("Arial", 16)
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Merken Sie sich diese Zeichenkette.",
            font=("Arial", 14)
        ).pack(pady=10)

        tk.Label(
            frame,
            text=self.test.formatted_sequence(),
            font=("Consolas", 42, "bold")
        ).pack(pady=35)

        tk.Label(
            frame,
            text="Nach 8 Sekunden verschwindet die Zeichenkette.",
            font=("Arial", 12)
        ).pack(pady=10)

        self.after_id = self.after(self.DISPLAY_MS, self._show_blank_screen)

    def _show_blank_screen(self):
        """Zeigt zwischen Merken und Eingabe für 8 Sekunden einen leeren Bildschirm."""
        self.after_id = None
        self._clear()

        frame = tk.Frame(self)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Bitte warten...",
            font=("Arial", 24)
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Die Eingabe erscheint in 8 Sekunden.",
            font=("Arial", 13)
        ).pack(pady=10)

        self.after_id = self.after(self.BLANK_MS, self._show_input_screen)

    def _show_input_screen(self):
        """Zeigt die Eingabemaske für die zuvor präsentierte Zeichenkette."""
        self.after_id = None
        self._clear()
        self.current_entries = []

        frame = tk.Frame(self)
        frame.pack(expand=True)

        tk.Label(
            frame,
            text=f"Geben Sie die Zeichenkette ein ({len(self.test.current_sequence)} Zeichen).",
            font=("Arial", 18)
        ).pack(pady=20)

        input_frame = tk.Frame(frame)
        input_frame.pack(pady=20)

        if self.test.mode == "chunked":
            self._create_chunk_entries(input_frame)
        else:
            self._create_character_entries(input_frame)

        tk.Button(
            frame,
            text="Eingabe bestätigen",
            font=("Arial", 14),
            command=self._submit_answer
        ).pack(pady=25)

        if self.current_entries:
            self.current_entries[0].focus_set()

    def _create_character_entries(self, parent):
        """Erzeugt ein einzelnes Eingabefeld pro Zeichen für die normale Version."""
        for index in range(len(self.test.current_sequence)):
            entry = tk.Entry(parent, width=2, justify="center", font=("Consolas", 20))
            entry.grid(row=0, column=index, padx=4, pady=4)
            entry.bind("<KeyRelease>", lambda event, i=index: self._focus_next_character(event, i))
            self.current_entries.append(entry)

    def _create_chunk_entries(self, parent):
        """Erzeugt Eingabefelder für 3er-Pakete in der chunkbasierten Version."""
        for index, chunk in enumerate(self.test.chunks(self.test.current_sequence)):
            entry = tk.Entry(parent, width=5, justify="center", font=("Consolas", 20))
            entry.grid(row=0, column=index, padx=8, pady=4)
            tk.Label(parent, text=f"{len(chunk)} Zeichen").grid(row=1, column=index)
            entry.bind(
                "<KeyRelease>",
                lambda event, i=index, size=len(chunk): self._focus_next_chunk(event, i, size)
            )
            self.current_entries.append(entry)

    def _focus_next_character(self, event, index):
        """Begrenzt ein Zeichenfeld auf ein Zeichen und springt zum nächsten Feld."""
        if event.keysym in {"BackSpace", "Delete", "Left", "Right", "Tab", "Shift_L", "Shift_R"}:
            return

        entry = self.current_entries[index]
        text = entry.get().upper()[:1]
        entry.delete(0, tk.END)
        entry.insert(0, text)

        if text and index + 1 < len(self.current_entries):
            self.current_entries[index + 1].focus_set()

    def _focus_next_chunk(self, event, index, size):
        """Begrenzt ein Chunk-Feld auf seine Länge und springt danach weiter."""
        if event.keysym in {"BackSpace", "Delete", "Left", "Right", "Tab", "Shift_L", "Shift_R"}:
            return

        entry = self.current_entries[index]
        text = entry.get().upper()[:size]
        entry.delete(0, tk.END)
        entry.insert(0, text)

        if len(text) >= size and index + 1 < len(self.current_entries):
            self.current_entries[index + 1].focus_set()

    def _submit_answer(self):
        """Liest die Eingaben aus, speichert das Ergebnis und startet den nächsten Trial."""
        answer = "".join(entry.get().strip().upper() for entry in self.current_entries)
        self.test.submit_answer(answer)
        self._show_next_sequence()

    def _show_plot(self):
        """Zeigt nach dem letzten Trial den Scatterplot mit den gesammelten Ergebnissen."""
        self._clear()

        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(
            frame,
            text="Ergebnis: Fehler nach Zeichenkettenlänge",
            font=("Arial", 22)
        ).pack(pady=10)

        tk.Label(
            frame,
            text=f"Modus: {self.test.mode_label()} | CSV: {self.test.csv_file.name}",
            font=("Arial", 12)
        ).pack(pady=5)

        canvas = tk.Canvas(frame, width=850, height=520, bg="white")
        canvas.pack(pady=20)
        self._draw_scatter_plot(canvas)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Neuen Durchlauf starten",
            command=self._show_start_screen
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Zurück zum Menü",
            command=self.app.show_main_menu
        ).pack(side="left", padx=10)

    def _draw_scatter_plot(self, canvas):
        """Zeichnet Achsen, Raster und Messpunkte auf den übergebenen Canvas."""
        width = int(canvas["width"])
        height = int(canvas["height"])
        left = 70
        right = 30
        top = 35
        bottom = 65
        plot_width = width - left - right
        plot_height = height - top - bottom
        max_errors = max(
            [ShortMemoryTest.MAX_LENGTH] + [result.errors for result in self.test.results]
        )

        canvas.create_line(left, top + plot_height, left + plot_width, top + plot_height, width=2)
        canvas.create_line(left, top, left, top + plot_height, width=2)
        canvas.create_text(width / 2, height - 20, text="Zeichenkettenlänge", font=("Arial", 12))
        canvas.create_text(20, height / 2, text="Fehler", angle=90, font=("Arial", 12))

        for length in range(ShortMemoryTest.MIN_LENGTH, ShortMemoryTest.MAX_LENGTH + 1):
            x = self._scale(
                length,
                ShortMemoryTest.MIN_LENGTH,
                ShortMemoryTest.MAX_LENGTH,
                left,
                left + plot_width
            )
            canvas.create_line(x, top + plot_height, x, top + plot_height + 5)
            canvas.create_text(x, top + plot_height + 20, text=str(length), font=("Arial", 9))

        for errors in range(0, min(max_errors, 15) + 1):
            y = self._scale(errors, 0, max_errors, top + plot_height, top)
            canvas.create_line(left - 5, y, left, y)
            canvas.create_text(left - 18, y, text=str(errors), font=("Arial", 9))
            canvas.create_line(left, y, left + plot_width, y, fill="#eeeeee")

        for result in self.test.results:
            x = self._scale(
                result.length,
                ShortMemoryTest.MIN_LENGTH,
                ShortMemoryTest.MAX_LENGTH,
                left,
                left + plot_width
            )
            y = self._scale(result.errors, 0, max_errors, top + plot_height, top)
            jitter_x = random.uniform(-5, 5)
            jitter_y = random.uniform(-5, 5)
            canvas.create_oval(
                x + jitter_x - 5,
                y + jitter_y - 5,
                x + jitter_x + 5,
                y + jitter_y + 5,
                fill="#1f77b4",
                outline=""
            )

    def _scale(self, value, source_min, source_max, target_min, target_max):
        """Rechnet einen Wert aus einem Datenbereich in einen Pixelbereich um."""
        if source_max == source_min:
            return target_min
        ratio = (value - source_min) / (source_max - source_min)
        return target_min + ratio * (target_max - target_min)
