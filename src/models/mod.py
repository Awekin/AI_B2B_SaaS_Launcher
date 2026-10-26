# klasa Mod, opisuje jeden mod

from __future__ import annotations


class Mod:
    # konstruktor, zapisujemy dane moda tak jak na diagramie
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
        self._loader = loader.lower()  # male litery zeby Fabric i fabric byly tym samym
        # tu trzymamy tylko id innych modow, nie cale obiekty
        self._dependencies = list(dependencies or [])
        self._incompatible_with = list(incompatible_with or [])
        self._file_name = file_name

    # zeby mozna bylo odczytac id i nazwe z zewnatrz, ale nie zmienic
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    # sprawdza czy mod pasuje do wersji gry i loadera
    def is_compatible(self, game_version: str, loader: str) -> bool:
        return self._game_version == game_version and self._loader == loader.lower()

    # sprawdza czy mod nie gryzie sie z innym modem, konflikt moze byc zapisany w ktoryms z nich
    def conflicts_with(self, other: Mod) -> bool:
        return other._id in self._incompatible_with or self._id in other._incompatible_with

    # jak mod wyglada w print
    def __repr__(self) -> str:
        return f"Mod({self._name} {self._version}, {self._loader} {self._game_version})"
