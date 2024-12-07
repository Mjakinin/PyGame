import tkinter as tk
from tkinter import messagebox
import random

class ButtonPuzzle:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.grid_size = 3  # 3x3 Grid
        self.buttons = []
        self.states = []  # Speichert die Zustände der Buttons (True = an, False = aus)
        self.frame = tk.Frame(self.root, bg="black")  # Schwarzer Hintergrund
        self.frame.pack()
        self.create_puzzle()

    def create_puzzle(self):
        # Initialisiere die Buttons und Zustände (Zufällig an oder aus)
        for i in range(self.grid_size):
            row_buttons = []
            row_states = []
            for j in range(self.grid_size):
                state = random.choice([True, False])  # Zufälliger Zustand (an oder aus)
                btn = tk.Button(self.frame, width=6, height=3, font=("Helvetica", 16),
                                bg=self.get_button_color(state),
                                fg="white",  # Textfarbe weiß
                                highlightbackground="white",  # Rahmen weiß
                                command=lambda i=i, j=j: self.on_button_click(i, j))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(btn)
                row_states.append(state)
            self.buttons.append(row_buttons)
            self.states.append(row_states)

    def get_button_color(self, state):
        # Gibt die Farbe zurück basierend auf dem Zustand (True = an = grün, False = aus = rot)
        return "#00ff00" if state else "#ff0000"

    def toggle_button(self, i, j):
        # Zustand des Buttons umschalten
        self.states[i][j] = not self.states[i][j]
        self.buttons[i][j].config(bg=self.get_button_color(self.states[i][j]))

    def on_button_click(self, i, j):
        # Zustand des geklickten Buttons und der benachbarten Buttons ändern
        self.toggle_button(i, j)  # Geklickter Button
        # Benachbarte Buttons ändern (oben, unten, links, rechts)
        if i > 0:  # Oben
            self.toggle_button(i - 1, j)
        if i < self.grid_size - 1:  # Unten
            self.toggle_button(i + 1, j)
        if j > 0:  # Links
            self.toggle_button(i, j - 1)
        if j < self.grid_size - 1:  # Rechts
            self.toggle_button(i, j + 1)

        # Überprüfen, ob alle Buttons "an" (grün) sind
        if all(all(row) for row in self.states):  # Alle Buttons True?
            messagebox.showinfo("Erfolg", "Du hast das Knöpferästel gelöst!")
            self.on_complete()

    def destroy(self):
        self.frame.destroy()
