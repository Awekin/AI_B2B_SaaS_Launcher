# main, pokazuje przypadki uzycia UC01 i UC04 (razem z UC03) oraz co sie dzieje przy zlych danych (LAB 5)
# uruchomienie: python3 src/main.py

from models import LauncherError, Mod, ModpackManager


# wypisuje blad razem z nazwa klasy bledu, zeby bylo widac ktory to blad
def print_error(error: LauncherError) -> None:
    print(f"  Odrzucono [{type(error).__name__}]: {error}")


def main() -> None:
    manager = ModpackManager("data")

    # ---------- UC01 tworzenie modpacka ----------
    print("== UC01: tworzenie modpacka ==")
    pack = manager.create_modpack("Optymalizacja", "1.20.1", "fabric")
    print(f"  Utworzono: {pack}")

    print("\n== UC01: błędne dane ==")
    # kazda proba w osobnym try, lapiemy LauncherError czyli kazdy nasz blad
    try:
        manager.create_modpack("", "1.20.1", "fabric")  # pusta nazwa
    except LauncherError as error:
        print_error(error)

    try:
        manager.create_modpack("optymalizacja", "1.20.1", "fabric")  # taka nazwa juz jest
    except LauncherError as error:
        print_error(error)

    try:
        manager.create_modpack("Survival", "1.20.1", "minecraft")  # nie ma takiego loadera
    except LauncherError as error:
        print_error(error)

    try:
        manager.create_modpack("Survival", "najnowsza", "fabric")  # zla wersja gry
    except LauncherError as error:
        print_error(error)

    print(f"  Liczba modpacków po błędach: {len(manager.modpacks)}")

    # ---------- UC04 zarzadzanie modami ----------
    print("\n== UC04: dodawanie modów ==")
    # przykladowe mody wpisane recznie, pozniej beda brane z Modrinth
    mods = [
        Mod("fabric-api", "Fabric API", "0.92.2", "1.20.1", "fabric"),
        Mod("sodium", "Sodium", "0.5.13", "1.20.1", "fabric"),
        Mod("lithium", "Lithium", "0.11.2", "1.20.1", "fabric"),
    ]
    for mod in mods:
        pack.add_mod(mod)
        print(f"  Dodano: {mod}")

    print("\n== UC04 + UC03: błędne dane ==")
    try:
        pack.add_mod(Mod("sodium", "Sodium", "0.5.13", "1.20.1", "fabric"))  # juz jest w modpacku
    except LauncherError as error:
        print_error(error)

    try:
        pack.add_mod(Mod("create", "Create", "0.5.1", "1.20.1", "forge"))  # mod dla forge
    except LauncherError as error:
        print_error(error)

    try:
        # optifabric nie dziala razem z sodium, to jest UC03 sprawdzenie kompatybilnosci
        optifabric = Mod("optifabric", "OptiFabric", "1.14.3", "1.20.1", "fabric", incompatible_with=["sodium"])
        pack.add_mod(optifabric)
    except LauncherError as error:
        print_error(error)

    try:
        Mod("", "Bez id", "1.0", "1.20.1", "fabric")  # zly mod, nie powstanie nawet obiekt
    except LauncherError as error:
        print_error(error)

    try:
        pack.remove_mod("jei")  # takiego moda nie ma w modpacku
    except LauncherError as error:
        print_error(error)

    print("\n== UC04: wyłączenie moda ==")
    pack.toggle_mod("lithium")
    print("  Aktywne mody:", ", ".join(m.name for m in pack.get_active_mods()))
    # po wszystkich bledach modpack jest dalej poprawny, nic sie nie zepsulo
    print(f"  Stan modpacka: {pack}")


if __name__ == "__main__":
    main()
