import tkinter as tk
from tkinter import messagebox

class NachbarlaenderPuzzle:
    def __init__(self, parent, on_puzzle_complete):
        self.parent = parent
        self.on_puzzle_complete = on_puzzle_complete

        # Vorgabe der Nachbarländer
        self.expected_countries = {
            "Dänemark", "Polen", "Tschechien", "Österreich", 
            "Schweiz", "Frankreich", "Luxemburg", "Belgien", 
            "Niederlande"
        }

        # Puzzle Frame
        self.frame = tk.Frame(self.parent, bg="black")  # Hintergrund schwarz
        self.frame.pack(expand=True, fill="both")

        # Titel für das Puzzle
        title = tk.Label(
            self.frame,
            text="Trage alle Nachbarländer von Allemania auf!",
            font=("Helvetica", 16, "bold"),
            bg="black",
            fg="white"
        )
        title.grid(row=0, column=0, columnspan=2, pady=10)

        # Liste für die Einträge der Nachbarländer
        self.entries = []

        # Eingabefelder für die Nachbarländer
        for i in range(9):
            # Label für die Nummer
            label = tk.Label(
                self.frame,
                text=f"{i + 1}.",
                font=("Helvetica", 12),
                bg="black",
                fg="white"
            )
            label.grid(row=i + 1, column=0, padx=(10, 5), pady=5, sticky="e")

            # Eingabefeld für das Nachbarland
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
        self.submit_button.grid(row=10, column=0, columnspan=2, pady=20)

    def check_answer(self):
        # Gesammelte Einträge
        user_inputs = {entry.get().strip().capitalize() for entry in self.entries if entry.get().strip()}

        # Überprüfen, ob alle erwarteten Nachbarländer eingegeben wurden
        if user_inputs == self.expected_countries:
            messagebox.showinfo("Richtig", "Die Antwort ist korrekt!")
            self.on_puzzle_complete()
            self.hide_puzzle()
        else:
            fehlend = self.expected_countries - user_inputs
            falsch = user_inputs - self.expected_countries
            messagebox.showwarning(
                "Falsch",
                f"Deine Eingaben sind nicht korrekt.\n\nFehlende Länder:\n{', '.join(fehlend) if fehlend else 'Keine'}\n"
                f"Falsch eingegebene Länder:\n{', '.join(falsch) if falsch else 'Keine'}"
            )

    def hide_puzzle(self):
        self.frame.pack_forget()

    def destroy(self):
        self.frame.destroy()
