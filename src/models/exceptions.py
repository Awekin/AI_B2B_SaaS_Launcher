# wlasne bledy aplikacji
# wszystkie dziedzicza po LauncherError, bo kazdy z nich JEST bledem launchera
# dzieki temu w main.py mozna zlapac je wszystkie jednym except LauncherError


class LauncherError(Exception):
    # wspolny blad launchera
    pass


class ValidationError(LauncherError):
    # zle dane wejsciowe, np pusta nazwa, nieznany loader, zla wersja gry
    pass


class DuplicateError(LauncherError):
    # cos takiego juz istnieje, np modpack o tej nazwie albo mod w modpacku
    pass


class NotFoundError(LauncherError):
    # nie ma modpacka albo moda o takim id
    pass


class IncompatibleModError(LauncherError):
    # mod nie pasuje do wersji gry albo loadera modpacka
    pass


class ModConflictError(LauncherError):
    # mod koliduje z innym modem, ktory juz jest w modpacku
    pass
