import tkinter as tk
import random
from tkinter import messagebox

class RockPaperScissorsGame:
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete

        self.player_score = 0
        self.bot_score = 0

        self.frame = tk.Frame(self.root, bg="black")  # Hintergrund schwarz
        self.frame.pack()

        self.create_ui()

    def create_ui(self):
        # Überschrift
        self.label = tk.Label(
            self.frame, 
            text="Wähle: Schere, Stein oder Papier", 
            font=("Helvetica", 18), 
            bg="black", 
            fg="white"
        )
        self.label.pack(pady=20)

        # Buttons für Auswahl
        self.button_frame = tk.Frame(self.frame, bg="black")
        self.button_frame.pack()

        for choice in ["Schere", "Stein", "Papier"]:
            btn = tk.Button(
                self.button_frame, text=choice, 
                command=lambda choice=choice: self.player_choice(choice),
                font=("Helvetica", 16), 
                width=10, 
                bg="#1E90FF", fg="white", 
                relief="ridge"
            )
            btn.pack(side=tk.LEFT, padx=10)

        # Score-Anzeige
        self.score_label = tk.Label(
            self.frame, 
            text="Spieler: 0 | Bot: 0", 
            font=("Helvetica", 16), 
            bg="black", 
            fg="white"
        )
        self.score_label.pack(pady=20)

        # Timer-Label
        self.timer_label = tk.Label(
            self.frame, 
            text="", 
            font=("Helvetica", 14), 
            bg="black", 
            fg="yellow"
        )
        self.timer_label.pack(pady=10)

    def player_choice(self, player_choice):
        # Countdown anzeigen
        self.timer_label.config(text="3...")
        self.frame.after(1000, lambda: self.update_timer(player_choice, 2))

    def update_timer(self, player_choice, count):
        if count > 0:
            self.timer_label.config(text=f"{count}...")
            self.frame.after(1000, lambda: self.update_timer(player_choice, count - 1))
        else:
            self.timer_label.config(text="")
            self.resolve_round(player_choice)

    def resolve_round(self, player_choice):
        bot_choice = random.choice(["Schere", "Stein", "Papier"])
        result = self.determine_winner(player_choice, bot_choice)

        # Ergebnis anzeigen
        messagebox.showinfo(
            "Ergebnis", 
            f"Deine Wahl: {player_choice}\nBot's Wahl: {bot_choice}\n\n{result}"
        )

        # Score aktualisieren
        self.score_label.config(text=f"Spieler: {self.player_score} | Bot: {self.bot_score}")

        # Prüfen, ob jemand gewonnen hat
        if self.player_score >= 3:
            messagebox.showinfo("Gewonnen!", "Du hast das Spiel gewonnen!")
            self.on_complete()
        elif self.bot_score >= 3:
            messagebox.showinfo("Verloren!", "Der Bot hat gewonnen. Versuche es erneut!")
            self.reset_game()

    def determine_winner(self, player_choice, bot_choice):
        if player_choice == bot_choice:
            return "Unentschieden!"
        elif (player_choice == "Schere" and bot_choice == "Papier") or \
             (player_choice == "Stein" and bot_choice == "Schere") or \
             (player_choice == "Papier" and bot_choice == "Stein"):
            self.player_score += 1
            return "Du gewinnst die Runde!"
        else:
            self.bot_score += 1
            return "Der Bot gewinnt die Runde!"

    def reset_game(self):
        self.player_score = 0
        self.bot_score = 0
        self.score_label.config(text="Spieler: 0 | Bot: 0")
