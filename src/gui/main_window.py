# klasa MainWindow, pierwsze okno aplikacji (LAB 7)
# okno tylko pobiera dane od uzytkownika i pokazuje wynik
# cala logika jest dalej w ModpackManager, okno tylko wola jego metody

import tkinter as tk
from tkinter import messagebox, ttk

from models import LauncherError, ModpackManager

LOADERS = ["fabric", "forge", "neoforge", "quilt"]


class MainWindow:
    def __init__(self, root: tk.Tk, manager: ModpackManager) -> None:
        self.root = root
        self.manager = manager  # przez niego okno dostaje sie do logiki i bazy
        self.root.title("AI B2B SaaS Launcher")
        self.root.geometry("700x450")
        self.create_widgets()
        self.refresh_list()  # na starcie pokazujemy to co jest w bazie

    # buduje wszystkie elementy okna
    def create_widgets(self) -> None:
        # Frame grupuje pola formularza
        form = ttk.Frame(self.root, padding=10)
        form.pack(fill="x")

        ttk.Label(form, text="Nazwa modpacka:").grid(row=0, column=0, sticky="w", pady=2)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=2)

        ttk.Label(form, text="Wersja gry:").grid(row=1, column=0, sticky="w", pady=2)
        self.version_entry = ttk.Entry(form, width=30)
        self.version_entry.insert(0, "1.20.1")  # przykladowa wartosc
        self.version_entry.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(form, text="Loader:").grid(row=2, column=0, sticky="w", pady=2)
        # Combobox
        self.loader_box = ttk.Combobox(form, values=LOADERS, state="readonly", width=27)
        self.loader_box.current(0)
        self.loader_box.grid(row=2, column=1, sticky="w", pady=2)

        # przyciski, command= mowi ktora metoda ma sie uruchomic po kliknieciu
        buttons = ttk.Frame(self.root, padding=(10, 0))
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Utwórz modpack", command=self.create_modpack).pack(side="left")
        ttk.Button(buttons, text="Usuń zaznaczony", command=self.delete_modpack).pack(side="left", padx=5)

        # Treeview
        columns = ("name", "loader", "version", "mods", "created")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        self.table.heading("name", text="Nazwa")
        self.table.heading("loader", text="Loader")
        self.table.heading("version", text="Wersja gry")
        self.table.heading("mods", text="Liczba modów")
        self.table.heading("created", text="Utworzony")
        # szerokosc kolumn, razem mniej wiecej szerokosc okna
        self.table.column("name", width=200)
        self.table.column("loader", width=90)
        self.table.column("version", width=90)
        self.table.column("mods", width=100, anchor="center")
        self.table.column("created", width=140)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        # pasek na dole z informacja co sie stalo
        self.status_label = ttk.Label(self.root, text="", padding=(10, 0, 10, 10))
        self.status_label.pack(fill="x")

    # czysci tabele i wpisuje modpacki jeszcze raz z menedzera
    def refresh_list(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)
        for pack in self.manager.modpacks:
            # iid = id modpacka, dzieki temu przy usuwaniu wiemy ktory to modpack
            self.table.insert("", "end", iid=pack.id, values=(
                pack.name,
                pack.loader,
                pack.game_version,
                len(pack.mods),
                f"{pack.created_at:%Y-%m-%d %H:%M}",
            ))

    # akcja przycisku "Utworz modpack" (UC01)
    def create_modpack(self) -> None:
        # 1. bierzemy dane z pol
        name = self.name_entry.get()
        game_version = self.version_entry.get()
        loader = self.loader_box.get()
        try:
            # 2. wolamy logike, ona sprawdza dane i zapisuje do bazy
            pack = self.manager.create_modpack(name, game_version, loader)
        except LauncherError as error:
            # 3a. zle dane, pokazujemy okienko z bledem
            messagebox.showerror("Błąd", str(error))
            return
        # 3b. wszystko ok, odswiezamy tabele
        self.refresh_list()
        self.name_entry.delete(0, "end")
        self.status_label.config(text=f"Utworzono modpack '{pack.name}' i zapisano w bazie.")

    # akcja przycisku "Usun zaznaczony" (UC02)
    def delete_modpack(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Usuń modpack", "Najpierw zaznacz modpack w tabeli.")
            return
        modpack_id = selected[0]
        name = self.table.item(modpack_id, "values")[0]
        if not messagebox.askyesno("Usuń modpack", f"Na pewno usunąć '{name}'?"):
            return
        self.manager.delete_modpack(modpack_id)  # usuwa z listy i z bazy
        self.refresh_list()
        self.status_label.config(text=f"Usunięto modpack '{name}'.")
