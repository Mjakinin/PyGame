import tkinter as tk
import random
from tkinter import messagebox

class SlidingPuzzle:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.tiles = list(range(1, 9)) + [None]
        random.shuffle(self.tiles)
        self.frame = tk.Frame(self.root, bg="black")  # Hintergrund schwarz
        self.frame.pack()
        self.create_puzzle()

    def create_puzzle(self):
        self.buttons = []
        for i, value in enumerate(self.tiles):
            btn = tk.Button(
                self.frame, text=value if value else "", 
                width=6, height=3, font=("Helvetica", 16), 
                command=lambda i=i: self.move_tile(i),
                bg="black", fg="white",  # Hintergrund schwarz, Text weiß
                highlightbackground="white"  # Rahmen weiß
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

    def move_tile(self, index):
        empty_index = self.tiles.index(None)
        if (index % 3 == empty_index % 3 and abs(empty_index - index) == 3) or \
           (index // 3 == empty_index // 3 and abs(empty_index - index) == 1):
            self.tiles[empty_index], self.tiles[index] = self.tiles[index], self.tiles[empty_index]
            self.update_puzzle()

        if self.tiles == list(range(1, 9)) + [None]:
            messagebox.showinfo("Erfolg", "Du hast das Schiebepuzzle gelöst!")
            self.on_complete()

    def update_puzzle(self):
        for i, value in enumerate(self.tiles):
            self.buttons[i].config(text=value if value else "")

    def destroy(self):
        self.frame.destroy()