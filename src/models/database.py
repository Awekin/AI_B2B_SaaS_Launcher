# klasa Database, zapis i odczyt modpackow z bazy SQLite (LAB 6)
# cala komunikacja z baza jest tutaj, reszta programu nie pisze SQL

from __future__ import annotations

import sqlite3
from datetime import datetime

from .exceptions import LauncherError
from .mod import Mod
from .modpack import Modpack

# tabela modpacks, jeden wiersz to jeden obiekt Modpack
CREATE_MODPACKS = """
CREATE TABLE IF NOT EXISTS modpacks (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE COLLATE NOCASE,
    game_version TEXT NOT NULL,
    loader       TEXT NOT NULL,
    created_at   TEXT NOT NULL
)
"""

# tabela mods, jeden wiersz to jeden mod w jednym modpacku
# modpack_id to klucz obcy, tak w bazie zapisujemy relacje Modpack - Mod
CREATE_MODS = """
CREATE TABLE IF NOT EXISTS mods (
    id                INTEGER PRIMARY KEY,
    modpack_id        TEXT NOT NULL REFERENCES modpacks(id) ON DELETE CASCADE,
    mod_id            TEXT NOT NULL,
    name              TEXT NOT NULL,
    version           TEXT NOT NULL,
    game_version      TEXT NOT NULL,
    loader            TEXT NOT NULL,
    dependencies      TEXT NOT NULL DEFAULT '',
    incompatible_with TEXT NOT NULL DEFAULT '',
    file_name         TEXT NOT NULL DEFAULT '',
    enabled           INTEGER NOT NULL DEFAULT 1,
    UNIQUE (modpack_id, mod_id)
)
"""


class Database:
    def __init__(self, path: str) -> None:
        self._path = path
        # connect otwiera plik bazy, a jak go nie ma to tworzy nowy ------------------------------------------------------
        self._connection = sqlite3.connect(path)
        # w sqlite klucze obce trzeba wlaczyc recznie, bez tego CASCADE nie dziala
        self._connection.execute("PRAGMA foreign_keys = ON")
        self.create_tables()

    @property
    def path(self) -> str:
        return self._path

    # tworzy tabele jesli jeszcze ich nie ma, przy kolejnym uruchomieniu nic nie robi ------------------------------------------------------
    def create_tables(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(CREATE_MODPACKS)
        cursor.execute(CREATE_MODS)
        self._connection.commit()

    # zapisuje jeden modpack razem z modami
    # najpierw kasujemy stara wersje, potem wpisujemy aktualna, wszystko w jednej transakcji
    # wszedzie sa znaki ? zamiast sklejania tekstu, wartosci podaje sqlite (ochrona przed SQL injection)
    def save_modpack(self, modpack: Modpack) -> None:
        cursor = self._connection.cursor()
        try:
            # dzieki ON DELETE CASCADE to usuwa tez stare mody tego modpacka ------------------------------------------------------
            cursor.execute("DELETE FROM modpacks WHERE id = ?", (modpack.id,))
            cursor.execute(
                "INSERT INTO modpacks (id, name, game_version, loader, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    modpack.id,
                    modpack.name,
                    modpack.game_version,
                    modpack.loader,
                    modpack.created_at.isoformat(),  # data jako tekst np. 2026-11-16T10:30:00
                ),
            )
            for mod in modpack.mods:
                cursor.execute(
                    "INSERT INTO mods (modpack_id, mod_id, name, version, game_version, loader,"
                    " dependencies, incompatible_with, file_name, enabled)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        modpack.id,
                        mod.id,
                        mod.name,
                        mod.version,
                        mod.game_version,
                        mod.loader,
                        ",".join(mod.dependencies),  # lista id jako tekst po przecinku
                        ",".join(mod.incompatible_with),
                        mod.file_name,
                        1 if modpack.is_enabled(mod.id) else 0,  # sqlite nie ma typu bool
                    ),
                )
            self._connection.commit()  # dopiero commit zapisuje zmiany w pliku
        except sqlite3.Error:
            self._connection.rollback()  # jak cos poszlo nie tak, baza zostaje jak byla
            raise

    # usuwa modpack, mody usuna sie same przez CASCADE
    def delete_modpack(self, modpack_id: str) -> None:
        self._connection.execute("DELETE FROM modpacks WHERE id = ?", (modpack_id,))
        self._connection.commit()

    # czyta wszystkie modpacki z bazy i odtwarza z nich obiekty
    # obiekty tworzymy przez zwykle konstruktory i add_mod, wiec dane z bazy tez sa sprawdzane
    # zly rekord jest pomijany, program sie przez niego nie wysypie ------------------------------------------------------
    def load_modpacks(self) -> list[Modpack]:
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name, game_version, loader, created_at FROM modpacks ORDER BY created_at")
        modpacks = []
        for modpack_id, name, game_version, loader, created_at in cursor.fetchall():
            try:
                modpack = Modpack(modpack_id, name, game_version, loader, datetime.fromisoformat(created_at))
                self._load_mods(modpack)
                modpacks.append(modpack)
            except (LauncherError, ValueError) as error:
                print(f"  Uwaga: pominięto błędny rekord modpacka '{name}': {error}")
        return modpacks

    # czyta mody jednego modpacka i dodaje je do obiektu
    def _load_mods(self, modpack: Modpack) -> None:
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT mod_id, name, version, game_version, loader, dependencies, incompatible_with,"
            " file_name, enabled FROM mods WHERE modpack_id = ? ORDER BY id",
            (modpack.id,),
        )
        for row in cursor.fetchall():
            mod_id, name, version, game_version, loader, deps, incompatible, file_name, enabled = row
            mod = Mod(
                mod_id,
                name,
                version,
                game_version,
                loader,
                dependencies=_split(deps),
                incompatible_with=_split(incompatible),
                file_name=file_name,
            )
            modpack.add_mod(mod)
            if not enabled:
                modpack.toggle_mod(mod_id)

    # zamyka polaczenie z baza
    def close(self) -> None:
        self._connection.close()


# zamienia tekst "a,b" z bazy z powrotem na liste ["a", "b"], pusty tekst daje pusta liste
def _split(text: str) -> list[str]:
    return [item for item in text.split(",") if item]
