"""Klasa ModpackManager: przechowuje wszystkie modpacki użytkownika."""

from __future__ import annotations

import uuid

from .modpack import Modpack


class ModpackManager:
    def __init__(self, data_dir: str) -> None:
        # Kompozycja ModpackManager ◆— Modpack (1 — 0..*): menedżer sam tworzy modpacki i je przechowuje
        self._modpacks: list[Modpack] = []
        self._data_dir = data_dir

    @property
    def modpacks(self) -> list[Modpack]:
        return list(self._modpacks)

    def create_modpack(self, name: str, game_version: str, loader: str) -> Modpack:
        """Tworzy nowy, pusty modpack (UC01)."""
        modpack = Modpack(str(uuid.uuid4()), name, game_version, loader)
        self._modpacks.append(modpack)
        return modpack

    def delete_modpack(self, modpack_id: str) -> None:
        """Usuwa modpack; razem z nim znikają jego dane (kompozycja)."""
        self._modpacks = [m for m in self._modpacks if m.id != modpack_id]

    # Import/eksport, kopie zapasowe oraz save()/load() dodamy na kolejnych etapach (UC05–UC07, „Baza danych”)
