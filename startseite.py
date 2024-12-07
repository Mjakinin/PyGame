import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # Für die Bildbearbeitung und Anzeige
import os
import sys

def resource_path(relative_path):
    """Findet den Pfad zu einer Ressource, egal ob das Programm als .py oder .exe läuft."""
    try:
        base_path = sys._MEIPASS  # Temporärer Ordner für PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # Aktuelles Verzeichnis für .py

    return os.path.join(base_path, relative_path)

class StartScreen:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback
        self.root.title("vilip")
        self.root.attributes('-fullscreen', True)  # Vollbildmodus
        self.root.configure(bg='black')  # Schwarzer Hintergrund

        # Starte Bindung für Leertaste
        self.root.bind("<space>", self.start_text_sequence)

        # Erstelle ein Frame für die Hauptinhalte
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(expand=True)

        # Erstelle die Überschrift
        self.create_title()

        # Erstelle den Text für den Start
        self.start_label = tk.Label(self.main_frame, text="Press SPACE to start",
                                    font=("Helvetica", 20, "bold"), fg="white", bg="black")
        self.start_label.pack(pady=60)

        # Animation
        self.animate_start_label()
    
    def start_text_sequence(self, event):
        # Entferne den Startbildschirm
        self.root.unbind("<space>")
        self.main_frame.destroy()
        # Beginne mit der Textsequenz
        TextSequence(self.root, self.start_game_callback)

    def create_title(self):
        # Erstelle eine Überschrift mit farbigen Buchstaben
        title_frame = tk.Frame(self.main_frame, bg='black')
        title_frame.pack()

        # Geburtstagstitel: Erste Zeile
        title_text_1 = "Happy Birthday Philipp"
        colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#FF9933", "#33FFD1", "#FF3333", "#75FF33"]

        for letter in title_text_1:
            letter_label = tk.Label(title_frame, text=letter, font=("Helvetica", 60, "bold"),
                                    fg=random.choice(colors), bg='black')
            letter_label.pack(side=tk.LEFT, padx=5)
            self.animate_letter(letter_label)

        # Geburtstagstitel: Zweite Zeile
        title_frame_2 = tk.Frame(self.main_frame, bg='black')
        title_frame_2.pack(pady=20)

        title_text_2 = "und Selina"
        for letter in title_text_2:
            letter_label = tk.Label(title_frame_2, text=letter, font=("Helvetica", 40, "bold"),
                                    fg=random.choice(colors), bg='black')
            letter_label.pack(side=tk.LEFT, padx=3)
            self.animate_letter(letter_label)

    def animate_letter(self, label):
        # Funktion zur Animation der Buchstaben, damit sie blinken
        def blink():
            current_color = label.cget("fg")
            new_color = random.choice(["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#FF9933", "#33FFD1", "#FF3333", "#75FF33"])
            while new_color == current_color:
                new_color = random.choice(["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#FF9933", "#33FFD1", "#FF3333", "#75FF33"])
            label.config(fg=new_color)
            label.after(500, blink)  # Wiederhole alle 500ms

        blink()

    def animate_start_label(self):
        # Funktion, damit der Starttext blinkt
        def blink():
            current_color = self.start_label.cget("fg")
            new_color = "white" if current_color == "black" else "black"
            self.start_label.config(fg=new_color)
            self.start_label.after(400, blink)

        blink()


class TextSequence:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback

        # Texte: Sprechertexte (ungerade Indizes) und Spielerantworten (gerade Indizes)
        self.texts = [
            "Hallo Spoole, ich darf doch Spoole sagen?",
            "Wer... spricht da?",
            "Oh, echt jetzt? Du hast das ganze Programm gestartet und weißt nicht, wer ich bin? Soll ich mich jetzt beleidigt fühlen?",
            "Äh, was? Wer bist du?",
            "Naja, die Person, die das Programm geschrieben hat, du Troll! Also, hallo! Ich bin der, der dafür sorgt, dass du hier bist. Aber keine Sorge, ich bin nett. Meistens.",
            "Du hast das Programmiert? Was ist das hier für ein Ort?",
            "Das hier? Oh, nichts Besonderes, nur der Ort, an dem du deine Existenz hinterfragen wirst. Vielleicht ein paar lustige Minigames, die dir den Tag versauen... oder ihn retten, je nachdem.",
            "Minigames? Was muss ich tun?",
            "Tja, du wirst schon sehen, aber keine Panik! Ich sorge dafür, dass du nicht in den Abgrund stürzt... naja, hoffe ich.",
            "Ich soll also spielen? Und warum genau?",
            "Weil du keine Wahl hast, Spoole! Das ist das Spiel. Du musst die Prüfungen bestehen, um den Schlüssel zu finden. Kein Druck. Vielleicht ein bisschen.",
            "Ein Schlüssel? Was passiert, wenn ich gewinne?",
            "Was passiert, wenn du gewinnst? Nun, du bekommst ein bisschen Ruhm, ein bisschen Ehre. Vielleicht ein Steamkey... oder was auch immer dir wichtig ist.",
            "Und wenn ich verliere?",
            "Dann... ja, wir reden nicht darüber. Aber hey, du schaffst das schon! Wahrscheinlich.",
            "Ähm, okay, was kommt als Nächstes?",
            "Also, Spoole, die Reise beginnt. Aber bevor wir weitermachen... Na, mich nennt man auch den Gamemaster. Klingt cool, oder?",
            "Gamemaster? Von den Prankbros, wtf?",
            "Sprich mir nach: 'Ich verspreche, dass ich nicht schummeln werde und dieses Programm zu Ende spiele.",
            "Ich verspreche, dass ich nicht schummeln werde und dieses Programm zu Ende spiele."
        ]


        self.current_text_index = 0  # Start bei erstem Text
        self.text_label = None  # Label für Sprechertext
        self.answer_button = None  # Button für Spielerantwort
        self.animating = False  # Status der Animation
        self.current_char_index = 0  # Index für die Animation des Textes

        # Frame für die Textanzeige
        self.text_frame = tk.Frame(self.root, bg='black')
        self.text_frame.pack(expand=True)

        # Label für den Sprechertext
        self.text_label = tk.Label(
            self.text_frame,
            text="",
            font=("Helvetica", 20),
            fg="white",
            bg="black",
            wraplength=1000,
            justify="center"
        )
        self.text_label.pack(pady=0)

        # Button für die Spielerantwort
        self.answer_button = tk.Button(
            self.root,
            text="",
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="black",
            relief="flat",
            height=3,  # Button-Höhe in Zeilen
            width=50,  # Button-Breite in Zeichen
            wraplength=600,  # Lasse Text im Button umbrechen
            justify="center",
            command=self.next_text
        )
        self.answer_button.pack(pady=200)

        self.root.bind("<space>", lambda event: self.next_text())


        # Zeige den ersten Text (Sprechertext)
        self.show_text()

    def show_text(self):
        # Unterscheide zwischen Sprechertext (Label) und Spielerantwort (Button)
        if self.current_text_index % 2 == 0:  # Sprechertext
            self.current_char_index = 0  # Reset Index für Animation
            current_text = self.texts[self.current_text_index]
            self.animate_text(current_text)  # Starte die Animation
            if self.current_text_index + 1 < len(self.texts):
                next_answer = self.texts[self.current_text_index + 1]  # Nächste Spielerantwort
                self.answer_button.config(text=next_answer, state=tk.DISABLED)
            else:
                self.answer_button.config(text="Weiter", state=tk.DISABLED)  # Fallback
        else:  # Spielerantwort
            next_text_index = self.current_text_index + 1
            if next_text_index < len(self.texts):
                self.current_text_index += 1  # Gehe direkt zum nächsten Sprechertext
                self.show_text()
            else:
                self.text_frame.destroy()
                self.answer_button.destroy()
                Gamemaster(self.root, self.start_game_callback)

    def animate_text(self, text):
        """Zeige den Text Buchstabe für Buchstabe an."""
        if self.current_char_index < len(text):
            self.animating = True
            self.text_label.config(text=text[:self.current_char_index + 1])
            self.current_char_index += 1
            self.text_label.after(20, self.animate_text, text)
        else:
            self.animating = False
            self.answer_button.config(state=tk.NORMAL)  # Aktiviere den Button nach der Animation

    def next_text(self):
        if self.animating:
            # Beende die Animation sofort und zeige den gesamten Text
            current_text = self.texts[self.current_text_index]
            self.text_label.config(text=current_text)
            self.animating = False
            self.answer_button.config(state=tk.NORMAL)  # Button aktivieren
        else:
            # Gehe zum nächsten Text und zeige ihn
            self.current_text_index += 1
            if self.current_text_index < len(self.texts):
                self.show_text()
            else:
                self.text_frame.destroy()
                self.answer_button.destroy()
                Gamemaster(self.root, self.start_game_callback)




class Gamemaster:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.start_game_callback = start_game_callback

        # Erstelle ein Frame für die Anzeige
        self.frame = tk.Frame(self.root, bg='black')
        self.frame.pack(expand=True)

        # Bild hinzufügen
        self.show_image()

        # Text hinzufügen
        self.show_text()

        # Binde Leertaste, um das Spiel zu starten
        self.root.bind("<space>", self.start_game)

    def show_image(self):
        try:
            # Lade das Bild
            self.image = Image.open(resource_path("nö.jpg"))

            # Hole die Bildschirmgröße
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            # Passe das Bild an die Bildschirmgröße an
            self.image = self.image.resize((screen_width, screen_height))

            # Konvertiere das Bild für Tkinter
            self.photo = ImageTk.PhotoImage(self.image)

            # Erstelle ein Label, das das Bild anzeigt
            self.image_label = tk.Label(self.frame, image=self.photo, bg="black")
            self.image_label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            # Fehlerbehandlung, falls das Bild nicht geladen werden kann
            print(f"Fehler beim Laden des Bildes: {e}")
            error_label = tk.Label(self.frame, text="Bild konnte nicht geladen werden", font=("Helvetica", 20, "bold"),
                                fg="red", bg="black")
            error_label.pack(pady=20)


    def show_text(self):
        # Text anzeigen, am unteren Rand des Bildes
        text_label = tk.Label(
            self.frame,
            text="Mögen die Spiele beginnen",
            font=("Helvetica", 40, "bold"),
            fg="black"
        )
        # Positioniere den Text unten, zentriert horizontal
        text_label.place(relx=0.5, rely=0.95, anchor="center")




    def start_game(self, event):
        # Entferne das Frame und starte das Spiel
        self.frame.destroy()
        self.root.unbind("<space>")  # Unbind Leertaste
        self.start_game_callback()






# Funktion, um den Startbildschirm zu zeigen und nach Leertaste das Hauptspiel zu starten
def show_start_screen(root, start_game_callback):
    StartScreen(root, start_game_callback)


# Beispiel-Hauptspiel-Funktion
def start_game():
    messagebox.showinfo("Spiel gestartet", "Das Spiel hat begonnen!")


# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    show_start_screen(root, start_game)
    root.mainloop()
