import tkinter as tk
import random

class MemoryGame:
    def __init__(self, frame, on_complete_callback):
        self.frame = frame
        self.on_complete_callback = on_complete_callback

        self.cards = list("AABBCCDDEEFFGGHH")  # Paare aus Buchstaben
        random.shuffle(self.cards)  # Karten zufällig mischen

        self.selected_cards = []  # Speichert die gewählten Karten
        self.matched_cards = []  # Speichert die gefundenen Paare
        self.is_checking = False  # Verhindert Klicken während der Überprüfung

        self.buttons = []
        self.create_board()

        self.label = tk.Label(
            self.frame, text="Finde die Paare!", font=("Helvetica", 18), bg="black", fg="white"
        )
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

    def create_board(self):
        """Erstellt das Spielfeld mit verdeckten Karten."""
        for i in range(4):  # 4x4 Spielfeld
            for j in range(4):
                btn = tk.Button(
                    self.frame, text="", font=("Helvetica", 18), width=4, height=2,
                    bg="darkblue", fg="white", command=lambda idx=len(self.buttons): self.reveal_card(idx)
                )
                btn.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")  # Füge "sticky" hinzu, damit der Button die gesamte Zelle ausfüllt
                self.buttons.append(btn)
                self.frame.grid_columnconfigure(j, weight=1, uniform="equal")  # Stelle sicher, dass alle Spalten die gleiche Breite haben
                self.frame.grid_rowconfigure(i + 1, weight=1, uniform="equal")  # Stelle sicher, dass alle Zeilen die gleiche Höhe haben


    def reveal_card(self, index):
        """Zeigt die Karte an und überprüft, ob ein Paar gefunden wurde."""
        if self.is_checking or index in self.matched_cards or index in self.selected_cards:
            return  # Klick ignorieren, wenn Karten überprüft werden oder Karte schon gewählt wurde

        # Karte aufdecken
        self.buttons[index].config(text=self.cards[index], bg="white", state=tk.DISABLED)
        self.selected_cards.append(index)

        if len(self.selected_cards) == 2:  # Wenn zwei Karten gewählt wurden
            self.is_checking = True  # Blockiert weitere Klicks
            self.frame.after(1000, self.check_match)

    def check_match(self):
        """Überprüft, ob die gewählten Karten ein Paar sind."""
        card1, card2 = self.selected_cards
        if self.cards[card1] == self.cards[card2]:  # Wenn es ein Paar ist
            self.matched_cards.extend(self.selected_cards)
            self.label.config(text="Paar gefunden!")

            # Entferne den Klick-Befehl, statt den Button auf DISABLED zu setzen
            for idx in self.selected_cards:
                self.buttons[idx].config(
                    text=self.cards[idx], bg="lightgreen", state="normal", disabledforeground="black"
                )
                self.buttons[idx].config(command=lambda: None)  # Entfernt den Klick-Befehl
        else:
            # Karten verdecken
            for idx in self.selected_cards:
                self.buttons[idx].config(text="", bg="darkblue", state="normal")
            self.label.config(text="Kein Paar, versuche es erneut!")

        self.selected_cards = []
        self.is_checking = False  # Klicks wieder erlauben

        # Prüfen, ob das Spiel gewonnen ist
        if len(self.matched_cards) == len(self.cards):  # Alle Paare gefunden
            self.label.config(text="Alle Paare gefunden! Du hast gewonnen!")
            self.frame.after(2000, self.on_complete_callback)

