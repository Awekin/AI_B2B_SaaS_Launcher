# stare menu w terminalu z LAB 6, od LAB 7 glowny program to okno (main.py)
# zostawione do testow i do pokazania LAB 6
# uruchomienie: python3 src/console_menu.py

import os

from models import LauncherError, Mod, Modpack, ModpackManager

# folder data obok folderu src, tam powstanie plik database.db
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# wypisuje blad razem z nazwa klasy bledu, zeby bylo widac ktory to blad
def print_error(error: LauncherError) -> None:
    print(f"  Odrzucono [{type(error).__name__}]: {error}")


# wypisuje wszystkie modpacki razem z modami
def show_modpacks(manager: ModpackManager) -> None:
    if not manager.modpacks:
        print("  Baza jest pusta, nie ma żadnych modpacków.")
        return
    for number, pack in enumerate(manager.modpacks, start=1):
        print(f"  {number}. {pack.name} ({pack.loader} {pack.game_version}), "
              f"utworzony {pack.created_at:%Y-%m-%d %H:%M}")
        for mod in pack.mods:
            state = "włączony" if pack.is_enabled(mod.id) else "wyłączony"
            print(f"       - {mod.name} {mod.version} [{state}]")


# pyta o numer z listy, zwraca element albo None jak numer jest zly
def choose(items: list, label: str):
    answer = input(f"  Numer {label}: ").strip()
    if not answer.isdigit() or not 1 <= int(answer) <= len(items):
        print("  Nie ma takiego numeru.")
        return None
    return items[int(answer) - 1]


# UC01, dane wpisuje uzytkownik, wiec mozna pokazac bledne dane na zywo
def create_modpack(manager: ModpackManager) -> None:
    name = input("  Nazwa: ")
    game_version = input("  Wersja gry (np. 1.20.1): ")
    loader = input("  Loader (fabric, forge, neoforge, quilt): ")
    try:
        pack = manager.create_modpack(name, game_version, loader)  # tu jest INSERT do bazy
        print(f"  Utworzono i zapisano w bazie: {pack}")
    except LauncherError as error:
        print_error(error)


# UC02
def delete_modpack(manager: ModpackManager) -> None:
    show_modpacks(manager)
    pack = choose(manager.modpacks, "modpacka do usunięcia")
    if pack is not None:
        manager.delete_modpack(pack.id)  # tu jest DELETE w bazie
        print(f"  Usunięto: {pack.name}")


# UC06, po zmianie zapisujemy modpack, w bazie zmienia sie kolumna enabled
def toggle_mod(manager: ModpackManager) -> None:
    show_modpacks(manager)
    pack = choose(manager.modpacks, "modpacka")
    if pack is None:
        return
    if not pack.mods:
        print("  Ten modpack nie ma modów.")
        return
    for number, mod in enumerate(pack.mods, start=1):
        print(f"    {number}. {mod.name}")
    mod = choose(pack.mods, "moda")
    if mod is not None:
        pack.toggle_mod(mod.id)
        manager.save()
        state = "włączony" if pack.is_enabled(mod.id) else "wyłączony"
        print(f"  {mod.name} jest teraz {state}, zapisano w bazie.")


# dodaje mody do modpacka (UC04), zle mody sa odrzucane jak na LAB 5
def add_mods(pack: Modpack, mods: list) -> None:
    for mod in mods:
        try:
            pack.add_mod(mod)
            print(f"  Dodano do '{pack.name}': {mod}")
        except LauncherError as error:
            print_error(error)


# kilka przykladowych rekordow, zeby nie wpisywac wszystkiego recznie
# mody sa wpisane recznie, pozniej beda brane z Modrinth
def add_sample_data(manager: ModpackManager) -> None:
    try:
        pack = manager.create_modpack("Optymalizacja", "1.20.1", "fabric")
        add_mods(pack, [
            Mod("fabric-api", "Fabric API", "0.92.2", "1.20.1", "fabric"),
            Mod("sodium", "Sodium", "0.5.13", "1.20.1", "fabric"),
            Mod("lithium", "Lithium", "0.11.2", "1.20.1", "fabric"),
            # ten sie nie doda, bo koliduje z sodium (UC03)
            Mod("optifabric", "OptiFabric", "1.14.3", "1.20.1", "fabric", incompatible_with=["sodium"]),
        ])
        pack.toggle_mod("lithium")  # jeden mod wylaczony, zeby bylo widac ze to tez sie zapisuje

        pack = manager.create_modpack("Technika", "1.20.1", "forge")
        add_mods(pack, [
            Mod("create", "Create", "0.5.1", "1.20.1", "forge"),
            Mod("jei", "Just Enough Items", "15.2.0", "1.20.1", "forge"),
        ])
        manager.save()  # zapis modow do bazy
        print("  Przykładowe dane zapisane w bazie.")
    except LauncherError as error:
        print_error(error)  # np. jak przykladowe dane juz sa w bazie


def main() -> None:
    manager = ModpackManager(DATA_DIR)
    try:
        # odczyt danych zapisanych przy poprzednim uruchomieniu
        manager.load()
        print(f"== Wczytano z bazy {manager.database_path} ==")
        print(f"  Liczba modpacków: {len(manager.modpacks)}")
        show_modpacks(manager)

        while True:
            print("\n1 - pokaż modpacki")
            print("2 - utwórz modpack (UC01)")
            print("3 - usuń modpack (UC02)")
            print("4 - włącz / wyłącz mod (UC06)")
            print("5 - dodaj przykładowe dane (UC01 + UC04)")
            print("0 - wyjście")
            choice = input("Wybór: ").strip()
            if choice == "1":
                show_modpacks(manager)
            elif choice == "2":
                create_modpack(manager)
            elif choice == "3":
                delete_modpack(manager)
            elif choice == "4":
                toggle_mod(manager)
            elif choice == "5":
                add_sample_data(manager)
            elif choice == "0":
                break
            else:
                print("  Nieznana opcja.")
    except (EOFError, KeyboardInterrupt):
        print()  # ctrl+d albo ctrl+c, wychodzimy normalnie
    finally:
        # baza zamyka sie zawsze, nawet przy bledzie
        manager.close()
        print("Koniec. Dane zostały w bazie, uruchom program ponownie żeby je zobaczyć.")


if __name__ == "__main__":
    main()
