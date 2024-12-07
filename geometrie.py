import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """Findet den Pfad zu einer Ressource, egal ob das Programm als .py oder .exe läuft."""
    try:
        base_path = sys._MEIPASS  # Temporärer Ordner für PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")  # Aktuelles Verzeichnis für .py

    return os.path.join(base_path, relative_path)


class GeometrieRaetsel:
    def __init__(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.frame = tk.Frame(self.parent, bg="black")
        self.frame.pack(pady=20)

        self.image = Image.open(resource_path("kopie.png"))
        self.image.thumbnail((400, 400))  # Bildgröße anpassen
        self.photo = ImageTk.PhotoImage(self.image)

        self.image_label = tk.Label(self.frame, image=self.photo, bg="black")
        self.image_label.pack()