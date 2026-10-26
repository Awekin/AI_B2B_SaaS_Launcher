# main, pokazuje jak dzialaja klasy z diagramu (LAB 4)
# uruchomienie: python3 src/main.py

from models import Mod, ModpackManager


def main() -> None:
    manager = ModpackManager("data")

    # UC01 tworzenie modpacka
    print("== UC01: tworzenie modpacka ==")
    pack = manager.create_modpack("Optymalizacja", "1.20.1", "fabric")
    print(f"Utworzono: {pack}")

    # UC04 dodawanie modow
    print("\n== UC04: dodawanie modów ==")
    # przykladowe mody wpisane recznie, pozniej beda brane z Modrinth
    mods = [
        Mod("fabric-api", "Fabric API", "0.92.2", "1.20.1", "fabric"),
        Mod("sodium", "Sodium", "0.5.13", "1.20.1", "fabric"),
        Mod("lithium", "Lithium", "0.11.2", "1.20.1", "fabric"),
    ]
    for mod in mods:
        pack.add_mod(mod)
        print(f"Dodano: {mod}")

    # mod dla forge nie pasuje do modpacka fabric, add_mod rzuci blad i go lapiemy
    try:
        pack.add_mod(Mod("create", "Create", "0.5.1", "1.20.1", "forge"))
    except ValueError as error:
        print(f"Odrzucono: {error}")

    # UC04 wylaczenie moda, lithium zostaje w modpacku ale nie jest aktywny
    print("\n== UC04: wyłączenie moda ==")
    pack.toggle_mod("lithium")
    print("Aktywne mody:", ", ".join(m.name for m in pack.get_active_mods()))
    print(f"Stan modpacka: {pack}")


if __name__ == "__main__":
    main()
