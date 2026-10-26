"""Klasa Modpack: zestaw modów dla jednej wersji gry i jednego loadera."""

from __future__ import annotations

from datetime import datetime

from .mod import Mod


class Modpack:
    def __init__(self, modpack_id: str, name: str, game_version: str, loader: str) -> None:
        self._id = modpack_id
        self._name = name
        self._game_version = game_version
        self._loader = loader.lower()
        # Asocjacja Modpack — Mod (0..* — 0..*): modpack przechowuje referencje do obiektów Mod
        self._mods: list[Mod] = []
        # Id modów wyłączonych: zostają w modpacku, ale nie trafiają do gry
        self._disabled_mods: set[str] = set()
        self._created_at = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def add_mod(self, mod: Mod) -> None:
        """Dodaje mod; błąd, gdy mod już jest albo nie pasuje do wersji gry lub loadera."""
        if any(m.id == mod.id for m in self._mods):
            raise ValueError(f"Mod '{mod.name}' jest już w modpacku '{self._name}'.")
        if not mod.is_compatible(self._game_version, self._loader):
            raise ValueError(f"Mod '{mod.name}' nie pasuje do {self._loader} {self._game_version}.")
        self._mods.append(mod)

    def remove_mod(self, mod_id: str) -> None:
        """Usuwa mod z modpacka."""
        self._mods = [m for m in self._mods if m.id != mod_id]
        self._disabled_mods.discard(mod_id)

    def toggle_mod(self, mod_id: str) -> None:
        """Włącza lub wyłącza mod bez usuwania go z modpacka."""
        if mod_id in self._disabled_mods:
            self._disabled_mods.remove(mod_id)
        else:
            self._disabled_mods.add(mod_id)

    def get_active_mods(self) -> list[Mod]:
        """Mody, które faktycznie trafią do gry."""
        return [m for m in self._mods if m.id not in self._disabled_mods]

    def __repr__(self) -> str:
        return f"Modpack({self._name}, {self._loader} {self._game_version}, modów: {len(self._mods)})"
