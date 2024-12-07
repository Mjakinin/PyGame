import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from bundesland_puzzle import BundeslandPuzzle
from schiebepuzzle import SlidingPuzzle
from knöpfe import ButtonPuzzle
from schachrätsel import SchachPuzzle
from geometrie import GeometrieRaetsel
from startseite import StartScreen
from soduko import SimplestSudoku
from rockpaperscissors import RockPaperScissorsGame
from farben import ColorMemoryGame
from memory import MemoryGame
from nachbar import NachbarlaenderPuzzle
from PIL import Image, ImageTk
import webbrowser
import time
import ctypes


KEY_LENGTH = 15
DASH_INTERVAL = 5

import os
import sys

def resource_path(relative_path):
    """Findet den Pfad zu einer Ressource, egal ob das Programm als .py oder .exe läuft."""
    try:
        base_path = sys._MEIPASS  # Temporärer Ordner für PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # Aktuelles Verzeichnis für .py

    return os.path.join(base_path, relative_path)




# Beispielhafter Produktschlüssel (ohne Bindestriche)
key = "ATV3L4FCD2J0P54"

# Aufgaben und Antworten (hier als Beispiel)
tasks = [
    {"question": "Wie viele Bundesländer gibt es?", "answer": "16"},
    {"question": "Dann benenn die doch mal:", "answer": ""},
    {"question": "Hier startet das Schiebepuzzle!", "answer": ""},
    {"question": "Hier sind ein paar Troller unterwegs\nWer sagt hier die Wahrheit?\n\n"
            "NeverNoOne: brudi ich war es nicht\n"
            "Maxirano: NeverNoOne wars, ich sag die Wahrheit\n"
            "Seagullr6: Maxirano wars, ich bin der Ehrliche hier\n"
        ,"answer": "Maxirano"},
    {"question": "Wie heißt Marius sein Fitness-Idol?", "answer": "Bernhard Imhof"},
    {"question": "Hier startet das Knöpferästel!", "answer": ""},
    {"question": "Setze die Zahlenreihenfolge fort: 1,1,2,3,5,8,13,?", "answer": "21"},
    {"question": "Das Schachbrett-Rätsel", "answer": ""},
    {"question": "Das Geometrie-Rätsel", "answer": "10cm"},
    {"question": "", "answer": ""},
    {"question": "Soduko", "answer": ""},
    {"question": "Schere Stein Papier", "answer": ""},
    {"question": "Wie heißt Xayah's Ult (englisch)?", "answer": "Featherstorm"},
    {"question": "foo", "answer": ""},
    {"question": "foo", "answer": ""}
]


class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("vilip")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")  # Hintergrund des gesamten Fensters auf schwarz setzen
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.start_time = time.time()

        url = "https://youtu.be/6Wi9_QKJ_8A?si=GGuD60KGrq2QVUkV"
        webbrowser.open(url)

        self.show_start_screen()

    def show_start_screen(self):
        StartScreen(self.root, self.start_game)

    def start_game(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.current_index = 0
        self.revealed_key = ["_" for _ in range(KEY_LENGTH)]
        self.current_puzzle_frame = None

        self.key_frame = tk.Frame(self.root, bg="black")  # Hintergrund schwarz
        self.key_frame.grid(row=0, column=0, pady=10, sticky="n")

        self.main_frame = tk.Frame(self.root, bg="black")  # Hintergrund schwarz
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.create_widgets()
        self.update_key_display()
        self.load_question()

    def create_widgets(self):
        self.question_label = tk.Label(self.main_frame, text="", font=("Helvetica", 18), wraplength=700, bg="black", fg="white")  # Text weiß, Hintergrund schwarz
        self.question_label.grid(row=0, column=0, columnspan=1, pady=50, sticky="n")

        self.answer_entry = tk.Entry(self.main_frame, font=("Helvetica", 14), width=30, bg="black", fg="white", insertbackground="white")  # Text weiß, Hintergrund schwarz
        self.answer_entry.grid(row=2, column=0, padx=10, sticky="n")

        self.answer_entry.bind("<Return>", lambda event: self.check_answer())

        self.submit_button = tk.Button(self.main_frame, text="Check", command=self.check_answer, font=("Helvetica", 14), bg="green", fg="#FFFFFF", relief="ridge", borderwidth=2, highlightbackground="#34C759", highlightthickness=2)
        self.submit_button.grid(row=2, column=0, padx=10, sticky="e")

        self.button_frame = tk.Frame(self.main_frame, bg="black")  # Hintergrund schwarz
        self.button_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)

        self.skip_button = tk.Button(self.button_frame, text="Skip", command=self.skip_question, font=("Helvetica", 10), bg="red", fg="#FFFFFF", relief="ridge", borderwidth=2, highlightbackground="#FFC107", highlightthickness=2)
        self.skip_button.grid(row=1, column=2, padx=10, pady=10, sticky="se")

        # Cheat-Button hinzufügen
        #self.cheat_button = tk.Button(self.button_frame, text="Cheat", command=self.reveal_all_chars, font=("Helvetica", 10), bg="blue", fg="#FFFFFF", relief="ridge", borderwidth=2, highlightbackground="#0000FF", highlightthickness=2)
        #self.cheat_button.grid(row=1, column=0, padx=10, pady=10, sticky="sw")

    def reveal_all_chars(self):
        """Reveals all characters of the key at once."""
        self.revealed_key = list(key)  # Enthüllt den gesamten Schlüssel
        self.update_key_display()  # Aktualisiert die Anzeige des Schlüssels
        messagebox.showinfo("Cheat aktiviert", "Alle Zeichen wurden enthüllt!")




    def update_key_display(self):
        for widget in self.key_frame.winfo_children():
            widget.destroy()

        for i in range(KEY_LENGTH + (KEY_LENGTH // DASH_INTERVAL)):
            if i > 0 and i % (DASH_INTERVAL + 1) == DASH_INTERVAL and i != KEY_LENGTH + (KEY_LENGTH // DASH_INTERVAL) - 1:
                label = tk.Label(self.key_frame, text="-", font=("Helvetica", 18), bg="black", fg="white")  # Text weiß, Hintergrund schwarz
                label.grid(row=0, column=i, padx=5)
            else:
                actual_index = i - (i // (DASH_INTERVAL + 1))
                if actual_index < KEY_LENGTH:
                    char = self.revealed_key[actual_index]
                    label = tk.Label(self.key_frame, text=char, font=("Helvetica", 18), bg="black", fg="white")  # Text weiß, Hintergrund schwarz

                    label.bind("<Button-1>", lambda event, idx=actual_index: self.switch_to_question(idx))

                    if actual_index == self.current_index:
                        label.config(font=("Helvetica", 24, "bold"), fg="red")
                    else:
                        label.config(font=("Helvetica", 18))

                    label.grid(row=0, column=i, padx=5)

    def switch_to_question(self, index):
        self.clear_puzzle()
        self.current_index = index
        self.update_key_display()
        self.load_question()

    def clear_puzzle(self):
        if self.current_puzzle_frame:
            self.current_puzzle_frame.destroy()
            self.current_puzzle_frame = None

        self.answer_entry.grid_forget()
        self.submit_button.grid_forget()
        self.skip_button.grid_forget()

        self.answer_entry.grid(row=2, column=0, columnspan=3, pady=10, sticky="n")
        self.submit_button.grid()
        self.skip_button.grid(row=1, column=2, padx=10, pady=10, sticky="se")

    def load_question(self):
        if "_" not in self.revealed_key:
            self.submit_button.config(state=tk.DISABLED)
            self.skip_button.config(state=tk.DISABLED)
            self.submit_button.grid_forget()
            self.answer_entry.grid_remove()
            self.show_congratulations_image()
        elif self.current_index < len(tasks):
            self.clear_puzzle()
            task = tasks[self.current_index]

            self.question_label.config(text=task["question"])
            self.answer_entry.delete(0, tk.END)

            # Spiele basierend auf Index starten
            puzzle_map = {
                1: (BundeslandPuzzle, "Benenne die 16 Bundesländer! Trage die Namen ein:"),
                2: (SlidingPuzzle, "Löse das Schiebepuzzle!"),
                5: (ButtonPuzzle, "Löse das Knöpferästel!"),
                7: (SchachPuzzle, "Löse das Schachrätsel!\n\nPlatziere 5 weitere Damen, ohne dass sie sich bedrohen!"),
                8: (GeometrieRaetsel, "Löse das Geometrie-Rätsel!\n\nWie lang ist die rote Linie?"),
                9: (NachbarlaenderPuzzle, ""),
                10: (SimplestSudoku, "Löse das Sudoku-Rätsel!"),
                11: (RockPaperScissorsGame, "Schere, Stein, Papier - Erreiche 3 Punkte, um zu gewinnen!"),
                13: (ColorMemoryGame, "Farbe"),
                14: (MemoryGame, "Finde alle Paare!")
            }

            if self.current_index in puzzle_map:
                puzzle_class, label_text = puzzle_map[self.current_index]
                self.start_game_with_params(puzzle_class, label_text)
            else:
                self.answer_entry.grid()  # Zeigt Standard-Eingabe an


    def check_answer(self):
        answer = self.answer_entry.get().strip()
        correct_answer = tasks[self.current_index]["answer"]
        if answer.lower() == correct_answer.lower():
            self.reveal_next_char()
        else:
            self.show_error_popup()

    def show_error_popup(self):
        # Prüfen, ob bereits ein Fehlerfenster geöffnet ist
        if hasattr(self, "error_popup") and self.error_popup is not None and self.error_popup.winfo_exists():
            self.error_popup.lift()  # Bringt das vorhandene Fenster in den Vordergrund
            return

        self.error_popup = tk.Toplevel(self.root)
        self.error_popup.title("Falsche Antwort")
        self.error_popup.configure(bg="black")

        # Fenster zentrieren
        window_width = 400
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 25
        self.error_popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        try:
            # Bild laden und in der gewünschten Größe skalieren
            img = Image.open(resource_path("böse.jpg"))
            img = img.resize((window_width, window_height), Image.Resampling.LANCZOS)
            self.error_image = ImageTk.PhotoImage(img)

            # Canvas für das Bild erstellen
            canvas = tk.Canvas(self.error_popup, width=window_width, height=window_height, bg="black", highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            # Bild auf das Canvas setzen
            canvas.create_image(0, 0, anchor="nw", image=self.error_image)

            # Text über das Bild legen
            canvas.create_text(
                window_width // 2, 12,  # Position des Texts (zentriert oben)
                text="Raff dich gefälligst, das war falsch!", 
                font=("Helvetica", 14, "bold"), fill="black", width=window_width - 50
            )

            # Schließen-Button über dem Canvas platzieren
            close_button = tk.Button(
                self.error_popup, text="Schließen", command=self.close_error_popup, 
                font=("Helvetica", 14), bg="red", fg="white"
            )
            close_button.place(relx=0.5, rely=0.9, anchor="center")  # Zentrierter Button unten
            self.error_popup.bind("<Return>", lambda event: self.close_error_popup())
            
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Die Datei 'böse.jpg' wurde nicht gefunden.")

    def close_error_popup(self):
        if hasattr(self, "error_popup") and self.error_popup is not None:
            self.error_popup.destroy()
            self.error_popup = None





    def skip_question(self):
        self.clear_puzzle()
        self.current_index += 1; self.update_key_display()
        self.load_question()

    def reveal_next_char(self):
        self.clear_puzzle()
        self.revealed_key[self.current_index] = key[self.current_index]
        self.current_index += 1
        self.answer_entry.delete(0, tk.END)
        self.update_key_display()
        self.load_question()

    def on_puzzle_complete(self):
        self.reveal_next_char()
        self.submit_button.config(state=tk.NORMAL)
        self.answer_entry.grid()

    def start_game_with_params(self, puzzle_class, label_text, row=1, column=0, columnspan=3, pady=20):
        self.question_label.config(text=label_text)

        # Überprüfung, ob das Rätsel das Geometrie-Rätsel ist
        if puzzle_class != GeometrieRaetsel:
            self.submit_button.grid_forget()
            self.answer_entry.grid_remove()

        self.current_puzzle_frame = tk.Frame(self.main_frame, bg="black")
        self.current_puzzle_frame.grid(row=row, column=column, columnspan=columnspan, pady=pady)

        self.current_puzzle = puzzle_class(self.current_puzzle_frame, self.on_puzzle_complete)


    def show_congratulations_image(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()  # Entfernt alle vorhandenen Widgets in der main_frame

        # Bild laden
        try:
            img = Image.open(resource_path("chill.jpg"))
            img = img.resize((600, 600), Image.Resampling.LANCZOS)
            self.chill_image = ImageTk.PhotoImage(img)  # Verhindert, dass das Bild gelöscht wird

            # Oberes Label (über dem Bild)
            top_label = tk.Label(
                self.main_frame,
                text="Wenn deine Freunde dich abfucken an deinem Geburtstag, aber du eigentlich ein ganz entspannter Typ bist und die scheiße durchgezogen hast",
                font=("Helvetica", 24, "bold"),
                wraplength=600,  # Lasse Text im Button umbrechen
                bg="black",
                fg="gold"
            )
            top_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

            # Label mit dem Bild hinzufügen
            label = tk.Label(self.main_frame, image=self.chill_image, bg="black")
            label.grid(row=1, column=0, columnspan=3, pady=10, sticky="n")

            # Glückwunsch-Text unter dem Bild
            congrats_label = tk.Label(
                self.main_frame,
                text="Das ist ein Steam Key falls du es nicht gecheckt hast lol",
                font=("Helvetica", 18),
                bg="black",
                fg="white"
            )
            congrats_label.grid(row=2, column=0, columnspan=3, pady=10, sticky="n")

            # Event-Handler für die Tasteneingabe binden
            self.root.bind("<Return>", lambda event: self.show_final_message())
            self.root.bind("<space>", lambda event: self.show_final_message())
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Die Datei 'chill.jpg' wurde nicht gefunden.")

    def show_final_message(self):
        """Zeigt die finale Nachricht 'LG der scheng' an und fügt den Fake-Button hinzu."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()  # Entfernt alle Widgets in der main_frame

        # Finale Nachricht anzeigen
        final_message = tk.Label(
            self.main_frame,
            text="LG der scheng",
            font=("Helvetica", 36, "bold"),
            bg="black",
            fg="white"
        )
        final_message.grid(row=0, column=0, columnspan=3, pady=100, sticky="n")

        # Fake-Button hinzufügen
        fake_button = tk.Button(
            self.main_frame,
            text="Drück mich",
            font=("Helvetica", 18),
            bg="blue",
            fg="white",
            command=self.trigger_troll_effect
        )
        fake_button.grid(row=1, column=0, pady=50, sticky="n")

    def trigger_troll_effect(self):
        """Zeigt einen lustigen Effekt und ersetzt den Fake-Button durch den echten Button."""
        # Berechnung der vergangenen Zeit
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(int(elapsed_time), 60)

        # Lustige Nachricht mit der Laufzeit
        messagebox.showinfo(
            "endlich digger wie lange bruder", 
            f"du hast {minutes} Minuten und {seconds} Sekunden gebraucht!"
        )

        # Entfernt alle bisherigen Widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Zeigt die finale Nachricht erneut
        final_message = tk.Label(
            self.main_frame,
            text="LG der scheng",
            font=("Helvetica", 36, "bold"),
            bg="black",
            fg="white"
        )
        final_message.grid(row=0, column=0, columnspan=3, pady=100, sticky="n")

        # Echter Schließen-Button
        close_button = tk.Button(
            self.main_frame,
            text="Feierabend",
            font=("Helvetica", 18),
            bg="red",
            fg="white",
            command=self.root.destroy
        )
        close_button.grid(row=1, column=0, pady=50, sticky="n")

    def exit_fullscreen(self, event=None):
        """Verlässt den Vollbildmodus."""
        self.root.attributes('-fullscreen', False)
        
if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()