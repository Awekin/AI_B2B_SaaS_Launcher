# wspolne funkcje do sprawdzania danych, uzywaja ich Mod i Modpack

import re

from .exceptions import ValidationError

SUPPORTED_LOADERS = ("fabric", "forge", "neoforge", "quilt")
MAX_NAME_LENGTH = 50
# wersja gry w formacie 1.20 albo 1.20.1
GAME_VERSION_PATTERN = re.compile(r"\d+\.\d+(\.\d+)?")


# tekst nie moze byc pusty ani z samych spacji, zwraca go bez spacji na koncach
def require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"Pole '{field}' nie może być puste.")
    return value.strip()


# loader musi byc jednym z obslugiwanych, zwraca go malymi literami
def validate_loader(loader: str) -> str:
    loader = require_text(loader, "loader").lower()
    if loader not in SUPPORTED_LOADERS:
        raise ValidationError(
            f"Nieznany loader '{loader}'. Dozwolone: {', '.join(SUPPORTED_LOADERS)}."
        )
    return loader


# wersja gry musi wygladac jak 1.20.1
def validate_game_version(game_version: str) -> str:
    game_version = require_text(game_version, "wersja gry")
    if not GAME_VERSION_PATTERN.fullmatch(game_version):
        raise ValidationError(
            f"Niepoprawna wersja gry '{game_version}'. Oczekiwany format np. 1.20.1."
        )
    return game_version
