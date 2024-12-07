import tkinter as tk
from tkinter import messagebox


class SimplestSudoku:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete

        # Sehr einfaches Sudoku-Puzzle (0 = leer)
        self.puzzle = [
            [5, 3, 4, 0, 7, 8, 0, 1, 2],
            [6, 0, 2, 1, 9, 5, 3, 4, 0],
            [1, 9, 8, 3, 0, 0, 0, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 0, 3],
            [4, 2, 6, 8, 5, 3, 0, 9, 1],
            [7, 1, 3, 9, 2, 0, 8, 5, 6],
            [0, 6, 1, 0, 3, 7, 2, 8, 0],
            [2, 8, 0, 4, 1, 9, 6, 0, 5],
            [3, 4, 5, 2, 8, 6, 0, 7, 9],
        ]

        # Lösung
        self.solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]

        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack()
        self.create_grid()

    def create_grid(self):
        """Erstellt das Sudoku-Raster mit hervorgehobenen 3x3-Boxen."""
        self.entries = []
        for row in range(9):
            row_entries = []
            for col in range(9):
                value = self.puzzle[row][col]

                # Rahmen erstellen: Dickere Linien für 3x3-Boxen
                top_border = 3 if row % 3 == 0 else 1
                left_border = 3 if col % 3 == 0 else 1
                right_border = 3 if col == 8 else 1
                bottom_border = 3 if row == 8 else 1

                entry = tk.Entry(
                    self.frame,
                    width=2,
                    font=("Helvetica", 18),
                    justify="center",
                    bg="white" if value == 0 else "lightgray",
                    fg="black",
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=0,
                    bd=0,
                )

                # Rahmenlinie durch Padding
                entry.grid(
                    row=row,
                    column=col,
                    padx=(left_border, right_border),
                    pady=(top_border, bottom_border),
                )

                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled")  # Fixierte Werte nicht änderbar

                row_entries.append(entry)
            self.entries.append(row_entries)

        # "Überprüfen"-Button
        check_button = tk.Button(
            self.frame,
            text="Überprüfen",
            command=self.check_solution,
            font=("Helvetica", 14),
            bg="green",
            fg="white",
        )
        check_button.grid(row=9, column=0, columnspan=9, pady=10)

    def check_solution(self):
        """Prüft, ob die Eingabe korrekt ist."""
        for row in range(9):
            for col in range(9):
                if self.entries[row][col].get() == "":
                    messagebox.showwarning("Fehler", "Das Sudoku ist noch nicht vollständig!")
                    return
                try:
                    value = int(self.entries[row][col].get())
                except ValueError:
                    messagebox.showerror("Fehler", f"Ungültiger Wert in Feld ({row + 1}, {col + 1}).")
                    return
                if value != self.solution[row][col]:
                    messagebox.showerror("Fehler", "Das Sudoku ist falsch gelöst!")
                    return

        # Erfolgreiche Lösung
        messagebox.showinfo("Erfolg", "Du hast das Sudoku korrekt gelöst!")
        self.on_complete()

    def destroy(self):
        """Entfernt das Sudoku-Spiel."""
        self.frame.destroy()


# Hauptprogramm
if __name__ == "__main__":
    def on_complete():
        print("Sudoku gelöst!")

    root = tk.Tk()
    root.title("Einfaches Sudoku mit Boxen")
    app = SimplestSudoku(root, on_complete)
    root.mainloop()
