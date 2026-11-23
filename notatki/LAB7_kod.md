- Okno: [main.py:19](../src/main.py#L19)
- Widgety: Entry [:29](../src/gui/main_window.py#L29), Combobox [:39](../src/gui/main_window.py#L39), Treeview [:51](../src/gui/main_window.py#L51)
- Przyciski: [:46](../src/gui/main_window.py#L46), [:47](../src/gui/main_window.py#L47)
- Metoda po kliknięciu: [:84](../src/gui/main_window.py#L84)
- Kod GUI: `src/gui/main_window.py`
- Logika + SQLite: [:91](../src/gui/main_window.py#L91) → [modpack_manager.py:31](../src/models/modpack_manager.py#L31)

Co dzieje się po kliknięciu? — `command=` woła `create_modpack`, ona bierze dane przez `get()` i woła `ModpackManager.create_modpack`, który zapisuje w SQLite. Okno odświeża tabelę albo pokazuje błąd.

Gdzie jest ta metoda? — `src/gui/main_window.py`, linia 84. Logika: `src/models/modpack_manager.py`, linia 31.

Połączenie z logiką i SQLite — okno woła tylko metody `ModpackManager`: GUI → logika → baza.
