"""Klasa Mod: opis jednej modyfikacji (wersja, loader, zależności, konflikty)."""

from __future__ import annotations


class Mod:
    def __init__(
        self,
        mod_id: str,
        name: str,
        version: str,
        game_version: str,
        loader: str,
        dependencies: list[str] | None = None,
        incompatible_with: list[str] | None = None,
        file_name: str = "",
    ) -> None:
        self._id = mod_id
        self._name = name
        self._version = version
        self._game_version = game_version
        self._loader = loader.lower()
        # Zależności i konflikty to listy identyfikatorów innych modów
        self._dependencies = list(dependencies or [])
        self._incompatible_with = list(incompatible_with or [])
        self._file_name = file_name

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def is_compatible(self, game_version: str, loader: str) -> bool:
        """Czy mod pasuje do wersji gry i loadera."""
        return self._game_version == game_version and self._loader == loader.lower()

    def conflicts_with(self, other: Mod) -> bool:
        """Czy mod koliduje z innym modem (konflikt może być zapisany po dowolnej stronie)."""
        return other._id in self._incompatible_with or self._id in other._incompatible_with

    def __repr__(self) -> str:
        return f"Mod({self._name} {self._version}, {self._loader} {self._game_version})"
