"""Punkt wejścia aplikacji: demonstracja modelu z diagramu klas (LAB 4).

Uruchomienie: python3 src/main.py
"""

from models import Mod, ModpackManager


def main() -> None:
    manager = ModpackManager("data")

    print("== UC01: tworzenie modpacka ==")
    pack = manager.create_modpack("Optymalizacja", "1.20.1", "fabric")
    print(f"Utworzono: {pack}")

    print("\n== UC04: dodawanie modów ==")
    # Przykładowe dane; na kolejnych etapach mody będą pobierane z repozytorium (Modrinth)
    mods = [
        Mod("fabric-api", "Fabric API", "0.92.2", "1.20.1", "fabric"),
        Mod("sodium", "Sodium", "0.5.13", "1.20.1", "fabric"),
        Mod("lithium", "Lithium", "0.11.2", "1.20.1", "fabric"),
    ]
    for mod in mods:
        pack.add_mod(mod)
        print(f"Dodano: {mod}")

    try:
        pack.add_mod(Mod("create", "Create", "0.5.1", "1.20.1", "forge"))
    except ValueError as error:
        print(f"Odrzucono: {error}")

    print("\n== UC04: wyłączenie moda ==")
    pack.toggle_mod("lithium")
    print("Aktywne mody:", ", ".join(m.name for m in pack.get_active_mods()))
    print(f"Stan modpacka: {pack}")


if __name__ == "__main__":
    main()
