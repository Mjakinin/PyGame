import tkinter as tk
import random

class ColorMemoryGame:
    def __init__(self, frame, on_complete_callback):
        self.frame = frame
        self.on_complete_callback = on_complete_callback

        self.colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        self.sequence = []  # Speichert die zufällige Sequenz
        self.user_sequence = []  # Speichert die Eingabe des Spielers

        self.label = tk.Label(
            self.frame, text="Farben merken!", font=("Helvetica", 18), bg="black", fg="white"
        )
        self.label.pack(pady=20)

        self.start_button = tk.Button(
            self.frame, text="Spiel starten", command=self.start_game,
            font=("Helvetica", 14), bg="green", fg="white"
        )
        self.start_button.pack(pady=10)

        self.color_buttons = []
        for color in self.colors:
            button = tk.Button(
                self.frame, bg=color, width=10, height=2, state=tk.DISABLED,
                relief="ridge", bd=5,  # Rahmen initial sichtbar
                command=lambda c=color: self.handle_user_input(c)
            )
            self.color_buttons.append(button)
            button.pack(pady=5)

    def start_game(self):
        """Startet das Spiel und erzeugt eine zufällige Sequenz."""
        self.sequence = random.sample(self.colors, len(self.colors))  # Erzeugt 6 Farben in zufälliger Reihenfolge
        self.user_sequence = []
        self.label.config(text="Farben merken!")
        self.start_button.config(state=tk.DISABLED)
        self.show_sequence()

    def show_sequence(self):
        """Zeigt die Farben der Sequenz nacheinander an."""
        self.disable_buttons()

        def flash_next_color(index):
            if index < len(self.sequence):
                # Alle Buttons unsichtbar machen (schwarz und ohne Rahmen)
                for button in self.color_buttons:
                    button.config(bg="black", relief="flat", bd=0)

                # Die nächste Farbe aufleuchten lassen
                color = self.sequence[index]
                button = next(b for b in self.color_buttons if b["bg"] == "black" and b.cget("bg") != color)
                button.config(bg=color, relief="ridge", bd=5)  # Farbe sichtbar machen und Rahmen aktivieren

                # Nach 1 Sekunde wieder ausblenden
                self.frame.after(1000, lambda: button.config(bg="black", relief="flat", bd=0))
                self.frame.after(1200, lambda: flash_next_color(index + 1))  # Nächste Farbe anzeigen
            else:
                self.frame.after(500, self.enable_buttons)  # Nach der Sequenz Tasten aktivieren

        flash_next_color(0)

    def enable_buttons(self):
        """Aktiviert die Tasten für die Benutzereingabe."""
        self.label.config(text="Jetzt bist du dran! Wiederhole die Sequenz.")
        for button, color in zip(self.color_buttons, self.colors):
            button.config(bg=color, relief="ridge", bd=5, state=tk.NORMAL)  # Originalfarbe und Rahmen wiederherstellen

    def disable_buttons(self):
        """Deaktiviert alle Tasten."""
        for button in self.color_buttons:
            button.config(state=tk.DISABLED)

    def handle_user_input(self, color):
        """Verarbeitet die Eingabe des Spielers."""
        self.user_sequence.append(color)
        if self.user_sequence == self.sequence:
            self.label.config(text="Richtig! Du hast gewonnen!")
            self.disable_buttons()
            self.frame.after(2000, self.on_complete_callback)  # Signalisiert der Haupt-App, dass das Spiel abgeschlossen ist
        elif self.user_sequence != self.sequence[:len(self.user_sequence)]:
            self.label.config(text="Falsch! Versuch es nochmal.")
            self.disable_buttons()
            self.start_button.config(state=tk.NORMAL)
