import tkinter as tk
from tkinter import messagebox

class BundeslandPuzzle:
    def __init__(self, parent, on_puzzle_complete):
        self.parent = parent
        self.on_puzzle_complete = on_puzzle_complete

        # Vorgabe der Bundesland-Anfangsbuchstaben
        self.expected_counts = {
            'B': 5,  # Berlin, Brandenburg, Bremen, Bayern, Baden-Württemberg
            'H': 2,  # Hessen, Hamburg
            'M': 1,  # Mecklenburg-Vorpommern
            'N': 2,  # Niedersachsen, Nordrhein-Westfalen
            'R': 1,  # Rheinland-Pfalz
            'S': 4,  # Sachsen, Sachsen-Anhalt, Schleswig-Holstein, Saarland
            'T': 1   # Thüringen
        }

        # Puzzle Frame
        self.frame = tk.Frame(self.parent, bg="black")  # Hintergrund schwarz
        self.frame.pack(expand=True, fill="both")

        # Liste für die Einträge der Bundesländer
        self.entries = []

        # Titel für das Puzzle
        title = tk.Label(
            self.frame,
            text="Trage die 16 Bundesländer ein:",
            font=("Helvetica", 16, "bold"),
            bg="black",
            fg="white"
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Einträge für die Bundesländer (16 leere Einträge)
        for i in range(16):
            # Label für die Nummer
            label = tk.Label(
                self.frame,
                text=f"{i + 1}.",
                font=("Helvetica", 12),
                bg="black",
                fg="white"
            )
            label.grid(row=i + 1, column=0, padx=(10, 5), pady=5, sticky="e")

            # Eingabefeld für das Bundesland
            entry = tk.Entry(
                self.frame,
                font=("Helvetica", 12),
                width=30,
                bg="black",
                fg="white",
                insertbackground="white"  # Cursor weiß
            )
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries.append(entry)

        # Button zum Überprüfen der Antwort
        self.submit_button = tk.Button(
            self.frame,
            text="Überprüfen",
            command=self.check_answer,
            font=("Helvetica", 14),
            bg="#34C759",
            fg="white",
            relief="ridge",
            borderwidth=2
        )
        self.submit_button.grid(row=17, column=0, columnspan=2, pady=20)

    def check_answer(self):
        # Zählen der Anfangsbuchstaben
        counts = {letter: 0 for letter in self.expected_counts.keys()}

        for entry in self.entries:
            bundesland = entry.get().strip().capitalize()
            if bundesland:  # Stelle sicher, dass das Feld nicht leer ist
                first_letter = bundesland[0]
                if first_letter in counts:
                    counts[first_letter] += 1

        # Überprüfen, ob die Anzahl der Anfangsbuchstaben mit den Vorgaben übereinstimmt
        if counts == self.expected_counts:
            messagebox.showinfo("Richtig", "Die Antwort ist korrekt!")
            self.on_puzzle_complete()
            self.hide_puzzle()
        else:
            messagebox.showwarning(
                "Falsch",
                f"Die Antwort ist leider falsch.\n\nErwartete Verteilung:\n{self.expected_counts}\n\nDeine Eingaben:\n{counts}"
            )

    def hide_puzzle(self):
        self.frame.pack_forget()

    def destroy(self):
        self.frame.destroy()
