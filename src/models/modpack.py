# klasa Modpack, zestaw modow dla jednej wersji gry i jednego loadera

from __future__ import annotations

from datetime import datetime

from .mod import Mod


class Modpack:
    # konstruktor, atrybuty jak na diagramie
    def __init__(self, modpack_id: str, name: str, game_version: str, loader: str) -> None:
        self._id = modpack_id
        self._name = name
        self._game_version = game_version
        self._loader = loader.lower()
        # asocjacja z Mod, modpack trzyma mody ale ich nie tworzy
        self._mods: list[Mod] = []
        # id wylaczonych modow, zostaja w modpacku ale nie ida do gry
        self._disabled_mods: set[str] = set()
        self._created_at = datetime.now()  # data utworzenia

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    # dodaje mod, ale najpierw sprawdza czy go juz nie ma i czy pasuje
    def add_mod(self, mod: Mod) -> None:
        if any(m.id == mod.id for m in self._mods):
            raise ValueError(f"Mod '{mod.name}' jest już w modpacku '{self._name}'.")
        # pytamy sam mod czy pasuje do naszej wersji i loadera
        if not mod.is_compatible(self._game_version, self._loader):
            raise ValueError(f"Mod '{mod.name}' nie pasuje do {self._loader} {self._game_version}.")
        self._mods.append(mod)

    # usuwa mod z listy i z wylaczonych
    def remove_mod(self, mod_id: str) -> None:
        self._mods = [m for m in self._mods if m.id != mod_id]
        self._disabled_mods.discard(mod_id)

    # wlacza albo wylacza mod, nie usuwa go
    def toggle_mod(self, mod_id: str) -> None:
        if mod_id in self._disabled_mods:
            self._disabled_mods.remove(mod_id)
        else:
            self._disabled_mods.add(mod_id)

    # zwraca tylko wlaczone mody, czyli te ktore pojda do gry
    def get_active_mods(self) -> list[Mod]:
        return [m for m in self._mods if m.id not in self._disabled_mods]

    # jak modpack wyglada w print
    def __repr__(self) -> str:
        return f"Modpack({self._name}, {self._loader} {self._game_version}, modów: {len(self._mods)})"
