# klasa ModpackManager, trzyma wszystkie modpacki uzytkownika

from __future__ import annotations

import os
import uuid

from .database import Database
from .exceptions import DuplicateError, NotFoundError
from .modpack import Modpack


class ModpackManager:
    def __init__(self, data_dir: str) -> None:
        # kompozycja z Modpack, menedzer sam tworzy modpacki i bez niego one nie istnieja
        self._modpacks: list[Modpack] = []
        self._data_dir = data_dir  # folder na dane, tu lezy plik bazy
        os.makedirs(data_dir, exist_ok=True)  # tworzy folder jak go nie ma
        # kompozycja z Database, menedzer sam otwiera baze (LAB 6)
        self._database = Database(os.path.join(data_dir, "database.db"))

    @property
    def modpacks(self) -> list[Modpack]:
        return list(self._modpacks)  # zwracamy kopie zeby nikt nie zmienil listy z zewnatrz

    @property
    def database_path(self) -> str:
        return self._database.path

    # tworzy nowy pusty modpack (UC01) i od razu zapisuje go w bazie
    def create_modpack(self, name: str, game_version: str, loader: str) -> Modpack:
        # konstruktor Modpack sprawdza nazwe, wersje i loader (scenariusz 3b)
        modpack = Modpack(str(uuid.uuid4()), name, game_version, loader)  # uuid daje unikalne id
        # nazwa musi byc unikalna, wielkosc liter nie ma znaczenia (scenariusz 3a)
        if any(m.name.lower() == modpack.name.lower() for m in self._modpacks):
            raise DuplicateError(f"Modpack o nazwie '{modpack.name}' już istnieje. Podaj inną nazwę.")
        self._database.save_modpack(modpack)  # najpierw baza, jak sie nie uda to lista sie nie zmieni
        self._modpacks.append(modpack)
        return modpack

    # usuwa modpack po id (UC02), z listy i z bazy
    def delete_modpack(self, modpack_id: str) -> None:
        if not any(m.id == modpack_id for m in self._modpacks):
            raise NotFoundError(f"Nie ma modpacka o id '{modpack_id}'.")
        self._database.delete_modpack(modpack_id)
        self._modpacks = [m for m in self._modpacks if m.id != modpack_id]

    # zapisuje wszystkie modpacki, wolamy po zmianach w modach (dodanie, wlaczenie, wylaczenie)
    def save(self) -> None:
        for modpack in self._modpacks:
            self._database.save_modpack(modpack)

    # wczytuje modpacki z bazy, wolamy przy starcie programu
    def load(self) -> None:
        self._modpacks = self._database.load_modpacks()

    # zamyka baze przy wyjsciu z programu
    def close(self) -> None:
        self._database.close()

    # import, eksport i kopie zapasowe dodamy na kolejnych labach
