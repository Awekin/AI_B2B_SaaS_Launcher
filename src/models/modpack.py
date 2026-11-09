# klasa Modpack, zestaw modow dla jednej wersji gry i jednego loadera

from __future__ import annotations

from datetime import datetime

from .exceptions import (
    DuplicateError,
    IncompatibleModError,
    ModConflictError,
    NotFoundError,
    ValidationError,
)
from .mod import Mod
from .validation import MAX_NAME_LENGTH, require_text, validate_game_version, validate_loader


class Modpack:
    # konstruktor, atrybuty jak na diagramie
    # dane sprawdzamy od razu, wiec zly modpack nie powstanie (UC01 scenariusz 3b)
    def __init__(self, modpack_id: str, name: str, game_version: str, loader: str) -> None:
        self._id = require_text(modpack_id, "id modpacka")
        self._name = require_text(name, "nazwa modpacka")
        if len(self._name) > MAX_NAME_LENGTH:
            raise ValidationError(f"Nazwa modpacka może mieć maksymalnie {MAX_NAME_LENGTH} znaków.")
        self._game_version = validate_game_version(game_version)
        self._loader = validate_loader(loader)
        # asocjacja z Mod, modpack trzyma mody ale ich nie tworzy
        self._mods: list[Mod] = []
        # id wylaczonych modow, zostaja w modpacku ale nie ida do gry
        self._disabled_mods: set[str] = set()
        self._created_at = datetime.now()  # data utworz.

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    # dodaje mod (UC04), przed dodaniem trzy sprawdzenia
    # jesli ktores nie przejdzie, mod nie zostaje dodany i modpack sie nie zmienia
    def add_mod(self, mod: Mod) -> None:
        # 1. czy mod juz nie jest w modpacku
        if self._find(mod.id) is not None:
            raise DuplicateError(f"Mod '{mod.name}' jest już w modpacku '{self._name}'.")
        # 2. pytamy sam mod czy pasuje do naszej wersji i loadera
        if not mod.is_compatible(self._game_version, self._loader):
            raise IncompatibleModError(
                f"Mod '{mod.name}' nie pasuje do modpacka ({self._loader} {self._game_version})."
            )
        # 3. sprawdzenie kompatybilnosci z innymi modami (UC03, scenariusz 5a z UC04)
        for other in self._mods:
            if mod.conflicts_with(other):
                raise ModConflictError(f"Mod '{mod.name}' koliduje z modem '{other.name}'.")
        self._mods.append(mod)

    # usuwa mod z listy i z wylaczonych
    def remove_mod(self, mod_id: str) -> None:
        mod = self._find(mod_id)
        if mod is None:
            raise NotFoundError(f"W modpacku '{self._name}' nie ma moda o id '{mod_id}'.")
        self._mods.remove(mod)
        self._disabled_mods.discard(mod_id)

    # wlacza albo wylacza mod, nie usuwa go
    def toggle_mod(self, mod_id: str) -> None:
        if self._find(mod_id) is None:
            raise NotFoundError(f"W modpacku '{self._name}' nie ma moda o id '{mod_id}'.")
        if mod_id in self._disabled_mods:
            self._disabled_mods.remove(mod_id)
        else:
            self._disabled_mods.add(mod_id)

    # zwraca tylko wlaczone mody, czyli te ktore pojda do gry
    def get_active_mods(self) -> list[Mod]:
        return [m for m in self._mods if m.id not in self._disabled_mods]

    # szuka moda po id, jak nie ma to zwraca None
    def _find(self, mod_id: str) -> Mod | None:
        for mod in self._mods:
            if mod.id == mod_id:
                return mod
        return None

    # jak modpack wyglada w print
    def __repr__(self) -> str:
        return f"Modpack({self._name}, {self._loader} {self._game_version}, modów: {len(self._mods)})"
