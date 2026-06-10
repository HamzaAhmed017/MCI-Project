import csv
import tempfile
import unittest
from pathlib import Path

from main.shortmemory.short_memory_logic import ShortMemoryTest


class ShortMemoryTestCase(unittest.TestCase):
    """Prüft die Logik des Kurzzeitgedächtnis-Tests ohne Tkinter-Eingaben."""

    def setUp(self):
        """Erstellt für jeden Test eine eigene temporäre CSV-Datei."""
        self.temp_directory = tempfile.TemporaryDirectory()
        self.csv_file = Path(self.temp_directory.name) / "results.csv"

    def tearDown(self):
        """Entfernt die temporären Testdateien."""
        self.temp_directory.cleanup()

    def create_test(self, mode="normal"):
        """Erstellt einen Testlauf, der Ergebnisse nur temporär speichert."""
        return ShortMemoryTest(mode, csv_file=self.csv_file)

    def test_trial_order(self):
        """Prüft dreimal jede Länge von 3 bis 15 in aufsteigender Reihenfolge."""
        memory_test = self.create_test()
        expected_trials = [
            length
            for length in range(3, 16)
            for _ in range(3)
        ]

        self.assertEqual(memory_test.trials, expected_trials)
        self.assertEqual(memory_test.total_trials(), 39)

    def test_generated_sequence_has_expected_length_and_characters(self):
        """Prüft Länge und erlaubte Zeichen jeder automatisch erzeugten Zeichenkette."""
        memory_test = self.create_test()

        for expected_length in memory_test.trials:
            sequence = memory_test.next_sequence()

            self.assertEqual(len(sequence), expected_length)
            self.assertTrue(set(sequence).issubset(set(memory_test.ALPHABET)))
            memory_test.submit_answer(sequence)

    def test_chunk_formatting(self):
        """Prüft die Aufteilung einer Zeichenkette in 3er-Pakete."""
        memory_test = self.create_test("chunked")
        memory_test.current_sequence = "ABCDEFGHIJ"

        self.assertEqual(
            memory_test.chunks(memory_test.current_sequence),
            ["ABC", "DEF", "GHI", "J"]
        )
        self.assertEqual(memory_test.formatted_sequence(), "ABC   DEF   GHI   J")

    def test_error_counting(self):
        """Prüft falsche, fehlende und zusätzlich eingegebene Zeichen."""
        memory_test = self.create_test()

        self.assertEqual(memory_test.count_errors("ABCDE", "ABCDE"), 0)
        self.assertEqual(memory_test.count_errors("ABCDE", "ABXDE"), 1)
        self.assertEqual(memory_test.count_errors("ABCDE", "ABC"), 2)
        self.assertEqual(memory_test.count_errors("ABC", "ABCXY"), 2)

    def test_complete_run_without_manual_input(self):
        """Durchläuft alle 39 Trials automatisch mit richtigen Antworten."""
        memory_test = self.create_test()

        while memory_test.has_next_trial():
            sequence = memory_test.next_sequence()
            result = memory_test.submit_answer(sequence)
            self.assertEqual(result.errors, 0)

        self.assertEqual(len(memory_test.results), 39)
        self.assertFalse(memory_test.has_next_trial())

        with self.csv_file.open(newline="", encoding="utf-8") as csv_file:
            rows = list(csv.DictReader(csv_file))

        self.assertEqual(len(rows), 39)
        self.assertTrue(all(int(row["errors"]) == 0 for row in rows))

    def test_answer_is_normalized_before_evaluation(self):
        """Prüft, dass Kleinbuchstaben und Leerzeichen korrekt normalisiert werden."""
        memory_test = self.create_test()
        memory_test.current_sequence = "ABC"

        result = memory_test.submit_answer(" abc ")

        self.assertEqual(result.answer, "ABC")
        self.assertEqual(result.errors, 0)

    def test_new_run_clears_existing_csv_data(self):
        """Prüft, dass ein neuer Testdurchlauf vorherige CSV-Daten entfernt."""
        self.csv_file.write_text("alte,daten\n1,2\n", encoding="utf-8")

        self.create_test()

        self.assertFalse(self.csv_file.exists())


if __name__ == "__main__":
    unittest.main()
