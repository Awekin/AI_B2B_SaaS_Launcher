# klasa ModpackManager, trzyma wszystkie modpacki uzytkownika

from __future__ import annotations

import uuid

from .exceptions import DuplicateError, NotFoundError
from .modpack import Modpack


class ModpackManager:
    def __init__(self, data_dir: str) -> None:
        # kompozycja z Modpack, menedzer sam tworzy modpacki i bez niego one nie istnieja
        self._modpacks: list[Modpack] = []
        self._data_dir = data_dir  # folder na dane, przyda sie przy zapisie na dysk

    @property
    def modpacks(self) -> list[Modpack]:
        return list(self._modpacks)  # zwracamy kopie zeby nikt nie zmienil listy z zewnatrz

    # tworzy nowy pusty modpack (UC01)
    def create_modpack(self, name: str, game_version: str, loader: str) -> Modpack:
        # konstruktor Modpack sprawdza nazwe, wersje i loader (scenariusz 3b)
        modpack = Modpack(str(uuid.uuid4()), name, game_version, loader)  # uuid daje unikalne id
        # nazwa musi byc unikalna, wielkosc liter nie ma znaczenia (scenariusz 3a)
        if any(m.name.lower() == modpack.name.lower() for m in self._modpacks):
            raise DuplicateError(f"Modpack o nazwie '{modpack.name}' już istnieje. Podaj inną nazwę.")
        self._modpacks.append(modpack)
        return modpack

    # usuwa modpack po id
    def delete_modpack(self, modpack_id: str) -> None:
        if not any(m.id == modpack_id for m in self._modpacks):
            raise NotFoundError(f"Nie ma modpacka o id '{modpack_id}'.")
        self._modpacks = [m for m in self._modpacks if m.id != modpack_id]

    # import, eksport, kopie zapasowe i save load dodamy na kolejnych labach
