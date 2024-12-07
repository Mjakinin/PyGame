import tkinter as tk
from tkinter import messagebox

class SchachPuzzle:
    def __init__(self, parent, on_puzzle_complete):
        self.parent = parent
        self.on_puzzle_complete = on_puzzle_complete

        # Initialisiere die Liste, die die Positionen der Damen speichert
        self.queens_positions = [(1, 5), (3, 6), (4, 3)]  # Initial queens: F7 (1,5), G5 (3,6), D4 (4,3)

        # Chessboard representation: 8x8 grid of buttons, Frame mit schwarzem Hintergrund um das Schachbrett
        self.board_frame = tk.Frame(self.parent, bg="black")  # Hintergrund des Rahmens schwarz
        self.board_frame.pack(pady=20)  # Abstand zum oberen Rand

        self.board_buttons = []
        self.selected_move = None

        # Create an 8x8 chessboard grid
        self.create_chessboard()

        # Button zum Überprüfen der Antwort
        self.submit_button = tk.Button(self.parent, text="Check", command=self.check_answer, font=("Helvetica", 14),
                                       bg="#34C759", fg="#FFFFFF", relief="ridge", borderwidth=2,
                                       highlightbackground="#34C759", highlightthickness=2)
        self.submit_button.pack(pady=20)  # Button unter dem Schachbrett platzieren

    def create_chessboard(self):
        """Creates an 8x8 chessboard of buttons with smaller size."""
        for row in range(8):
            button_row = []
            for col in range(8):
                button = tk.Button(self.board_frame, width=3, height=1, font=('Arial', 12),
                                   command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col, padx=1, pady=1)  # padding hinzugefügt, um das Design zu verbessern
                button_row.append(button)
            self.board_buttons.append(button_row)

        # Update the board with existing queens
        self.update_board()

    def on_square_click(self, row, col):
        """Handle a square being clicked for queen placement or removal."""
        # Überprüfe, ob auf einem Feld bereits eine Dame steht
        if (row, col) in self.queens_positions:
            # Erlaube das Entfernen der Dame, außer es handelt sich um eine vorgegebene Dame
            if (row, col) in [(1, 5), (3, 6), (4, 3)]:
                messagebox.showerror("Fehler", "Diese Dame kann nicht entfernt werden!")
            else:
                # Entferne die Dame, wenn es keine der fixierten Damen ist
                self.queens_positions.remove((row, col))
                self.update_board()
        else:
            # Stelle sicher, dass nur 8 Damen insgesamt platziert werden können
            if len(self.queens_positions) >= 8:
                messagebox.showerror("Fehler", "Du hast bereits 8 Damen platziert!")
                return

            # Füge die neue Dame hinzu
            self.queens_positions.append((row, col))
            self.update_board()

    def update_board(self):
        """Updates the chessboard, showing queens and highlighting the selected move."""
        for row in range(8):
            for col in range(8):
                if (row, col) in self.queens_positions:
                    self.board_buttons[row][col].config(text='D', bg='light blue', fg="black")  # Dame hellblau, Text schwarz
                else:
                    # Passe die Farben der Felder wieder auf "weiß" und "grau" an
                    color = 'white' if (row + col) % 2 == 0 else 'gray'
                    self.board_buttons[row][col].config(text='', bg=color)

    def is_valid_move(self):
        """Check if the current placement of queens is valid (no queens threaten each other)."""
        for i, (q1_row, q1_col) in enumerate(self.queens_positions):
            for j, (q2_row, q2_col) in enumerate(self.queens_positions):
                if i != j:  # Vermeide es, dieselbe Dame zu vergleichen
                    # Prüfe, ob sie in derselben Reihe, Spalte oder Diagonale stehen
                    if q1_row == q2_row or q1_col == q2_col or abs(q1_row - q2_row) == abs(q1_col - q2_col):
                        return False
        return True

    def check_answer(self):
        """Checks if the puzzle is solved correctly (8 queens placed without threatening each other)."""
        if len(self.queens_positions) == 8:
            if self.is_valid_move():
                messagebox.showinfo("Richtig", "Du hast alle 8 Damen korrekt platziert!")
                self.on_puzzle_complete()
                self.hide_puzzle()
            else:
                messagebox.showerror("Falsch", "Eine oder mehrere Damen bedrohen sich gegenseitig. Versuche es erneut.")
        else:
            messagebox.showerror("Unvollständig", "Es sind noch nicht alle 8 Damen platziert.")

    def skip_puzzle(self):
        """Skip the puzzle."""
        self.on_puzzle_complete()
        self.hide_puzzle()

    def hide_puzzle(self):
        """Hides the current puzzle's widgets."""
        self.board_frame.pack_forget()
        self.submit_button.pack_forget()

# Example usage within a Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Schach Puzzle")
    root.geometry("600x600")  # Füge eine Fenstergröße hinzu
    root.configure(bg="black")  # Hintergrund des gesamten Fensters schwarz

    def puzzle_complete():
        messagebox.showinfo("Puzzle abgeschlossen", "Das Puzzle wurde abgeschlossen!")

    puzzle = SchachPuzzle(root, puzzle_complete)
    root.mainloop()
