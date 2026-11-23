# main, od LAB 7 tylko uruchamia aplikacje: tworzy menedzera, wczytuje baze i otwiera okno
# okno jest w gui/main_window.py, logika w models/
# uruchomienie: python3 src/main.py

import os
import tkinter as tk

from gui import MainWindow
from models import ModpackManager

# folder data obok folderu src, tam jest plik database.db
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

 
def main() -> None:
    manager = ModpackManager(DATA_DIR)  # logika + baza
    manager.load()  # dane z poprzedniego uruchomienia

    root = tk.Tk()  # glowne okno
    MainWindow(root, manager)  # buduje widgety w oknie
    root.mainloop()  # czeka na klikniecia

    manager.close()  # zamyk. bazy


if __name__ == "__main__":
    main()
