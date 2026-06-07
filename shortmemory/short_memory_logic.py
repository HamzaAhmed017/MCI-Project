import csv
import random
import string
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ShortMemoryResult:
    """Speichert das Ergebnis eines einzelnen Durchgangs."""

    timestamp: str
    mode: str
    length: int
    errors: int
    target: str
    answer: str


class ShortMemoryTest:
    """Enthält die testbezogene Logik für den Kurzzeitgedächtnis-Test."""

    MAX_LENGTH = 15
    REPETITIONS_PER_LENGTH = 3
    ALPHABET = string.ascii_uppercase + string.digits

    def __init__(self, mode, csv_file=None):
        """Initialisiert einen Testdurchlauf mit zufälliger Trial-Reihenfolge."""
        self.mode = mode
        self.csv_file = csv_file or Path(__file__).with_name("short_memory_results.csv")
        self.trials = self._create_trials()
        self.current_index = 0
        self.current_sequence = ""
        self.results = []

    def has_next_trial(self):
        """Gibt zurück, ob noch ein weiterer Trial vorhanden ist."""
        return self.current_index < len(self.trials)

    def total_trials(self):
        """Gibt die Gesamtanzahl der Trials im Durchlauf zurück."""
        return len(self.trials)

    def trial_number(self):
        """Gibt die aktuell angezeigte Trial-Nummer für die GUI zurück."""
        return self.current_index + 1

    def next_sequence(self):
        """Erzeugt die nächste Zeichenkette passend zur aktuellen Trial-Länge."""
        length = self.trials[self.current_index]
        self.current_sequence = self._create_sequence(length)
        return self.current_sequence

    def formatted_sequence(self):
        """Formatiert die aktuelle Zeichenkette je nach Modus normal oder in 3er-Paketen."""
        if self.mode != "chunked":
            return self.current_sequence
        return "   ".join(self.chunks(self.current_sequence))

    def submit_answer(self, answer):
        """Bewertet eine Antwort, speichert das Ergebnis und geht zum nächsten Trial."""
        answer = answer.strip().upper()
        result = ShortMemoryResult(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            mode=self.mode,
            length=len(self.current_sequence),
            errors=self.count_errors(self.current_sequence, answer),
            target=self.current_sequence,
            answer=answer,
        )

        self.results.append(result)
        self._write_result(result)
        self.current_index += 1
        return result

    def chunks(self, sequence):
        """Teilt eine Zeichenkette in Pakete mit maximal drei Zeichen auf."""
        return [sequence[index:index + 3] for index in range(0, len(sequence), 3)]

    def count_errors(self, target, answer):
        """Zählt alle abweichenden, fehlenden und zusätzlich eingegebenen Zeichen."""
        max_length = max(len(target), len(answer))
        return sum(
            1
            for index in range(max_length)
            if self._char_at(target, index) != self._char_at(answer, index)
        )

    def mode_label(self):
        """Gibt den ausgewählten Testmodus als lesbaren Text zurück."""
        return "3er-Pakete" if self.mode == "chunked" else "Normale Darstellung"

    def _create_trials(self):
        """Erstellt die 45 Trial-Längen und mischt ihre Reihenfolge zufällig."""
        trials = [
            length
            for length in range(1, self.MAX_LENGTH + 1)
            for _ in range(self.REPETITIONS_PER_LENGTH)
        ]
        random.shuffle(trials)
        return trials

    def _create_sequence(self, length):
        """Erzeugt eine zufällige Zeichenkette aus Großbuchstaben und Ziffern."""
        return "".join(random.choice(self.ALPHABET) for _ in range(length))

    def _write_result(self, result):
        """Hängt ein einzelnes Testergebnis an die CSV-Datei an."""
        self.csv_file.parent.mkdir(parents=True, exist_ok=True)
        file_exists = self.csv_file.exists()

        with self.csv_file.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=["timestamp", "mode", "length", "errors", "target", "answer"]
            )
            if not file_exists:
                writer.writeheader()
            writer.writerow(result.__dict__)

    def _char_at(self, value, index):
        """Liefert ein Zeichen an einer Position oder einen Leerwert außerhalb der Länge."""
        return value[index] if index < len(value) else ""
