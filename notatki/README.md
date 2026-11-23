# AI B2B SaaS Launcher — общие сведения

## Запуск проекта

Из корня репозитория (папка, где лежат `src/` и `notatki/`):

```bash
python3 src/main.py
```

На Mac Андрия перейти в эту папку можно так:

```bash
cd "/Users/awekin/Files/PK/Technologie obiektowe - Projekt/AI B2B SaaS Launcher"
```

Нужен Python 3.9 или новее (проверить: `python3 --version`). Сторонние библиотеки не нужны.

С LAB 7 программа открывает окно (Tkinter). Системный `python3` на Mac идёт со старым Tk 8.5, и окно с ним зависает. Поставь Python с новым Tk и запускай через него:

```bash
brew install python-tk@3.13
python3.13 src/main.py
```

Старое меню в терминале (LAB 6): `python3 src/console_menu.py`.

Данные хранятся в `data/database.db` (SQLite, LAB 6). Начать с пустой базы: `rm -f data/database.db`.

## О проекте

**Что это:** настоящий лаунчер Minecraft для работы с модами. Создаёт модпаки (наборы модов), сам подбирает зависимости, проверяет совместимость модов и запускает игру. Слова «AI B2B SaaS» — просто название, ИИ не планируется.

**Курс:** Technologie obiektowe (Politechnika Krakowska).
**Авторы:** Andrii Semeniuk, Dmytro Burkovskyi.
**Репозиторий:** https://github.com/Awekin/AI_B2B_SaaS_Launcher

**Решения по проекту:**
- платформа — macOS (в документации LAB 2 ещё написано «Windows .exe», требование RNF02 надо поправить);
- язык — Python; имена в коде на английском, комментарии и тексты программы на польском;
- лаунчер должен быть настоящим: Modrinth API, вход через Microsoft, установка загрузчика (Fabric/Forge), запуск игры;
- формат импорта/экспорта модпаков ещё не выбран.

**Предполагаемый стек:** Tkinter + ttk (интерфейс, так требует курс на LAB 7), `minecraft-launcher-lib` (установка и запуск игры, вход Microsoft), PyInstaller (сборка `.app`).

## Где что лежит

```
Technologie obiektowe - Projekt/
  AI B2B SaaS Launcher/        приложение (git-репозиторий)
    src/main.py                запуск: менеджер + база + окно
    src/console_menu.py        старое меню в терминале (LAB 6)
    src/gui/main_window.py     окно, класс MainWindow (LAB 7)
    src/models/                классы из диаграммы
    data/database.db           база SQLite (создаётся сама, не в git)
    notatki/                   эти заметки
  docs/                        список классов (PDF), диаграммы классов v1–v3, модель данных
  Przypadki Uzycia/            варианты использования (LAB 2)
  archiwum/lab4_pelna_wersja/  полная версия с 6 классами и Modrinth (на будущее)
```

## Классы

| Класс | Что делает | Статус |
|---|---|---|
| `Mod` | один мод | готов |
| `Modpack` | набор модов для одной версии игры и загрузчика | готов |
| `ModpackManager` | хранит, создаёт и удаляет модпаки, save/load | частично (нет импорта/экспорта и копий) |
| `Database` | запись и чтение модпаков в SQLite | готов (LAB 6) |
| `MainWindow` | главное окно: форма, кнопки, таблица | первая версия (LAB 7) |
| `ModRepository` | поиск и скачивание модов из Modrinth | позже (есть в архиве) |
| `ModResolver` | зависимости и конфликты | позже (есть в архиве) |
| `GameLauncher` | вход Microsoft и запуск игры | позже |
| ошибки в `exceptions.py` | свои исключения, все от `LauncherError` | готовы (LAB 5) |

## Варианты использования (диаграмма v2)

Актуальная версия — `Przypadki Uzycia/przypadki_uzycia_v2.md` (+ `.png`). Старая v1 оставлена для истории, номера в ней другие.

| UC | Название | В коде |
|---|---|---|
| UC01 | Utwórz modpack | ✔ `ModpackManager.create_modpack` |
| UC02 | Usuń modpack | ✔ `ModpackManager.delete_modpack` |
| UC03 | Sprawdź kompatybilność modów | ✔ проверка конфликтов в `add_mod` |
| UC04 | Dodaj mod do modpacka | ✔ `Modpack.add_mod` |
| UC05 | Usuń mod z modpacka | ✔ `Modpack.remove_mod` |
| UC06 | Włącz / wyłącz mod | ✔ `Modpack.toggle_mod` |
| UC07 | Pobierz brakujące mody (zależności) | позже (нужен Modrinth) |
| UC08 | Wyszukaj mod w katalogu | позже (нужен Modrinth) |
| UC09 | Importuj modpack z pliku | позже |
| UC10 | Eksportuj modpack do pliku | позже |
| UC11 | Utwórz kopię zapasową modpacka | позже |
| UC12 | Przywróć modpack z kopii | позже |
| UC13 | Zaloguj się kontem Microsoft | позже |
| UC14 | Uruchom grę z modpackiem | позже |

## Лабы

| Лаба | Тема | Заметки |
|---|---|---|
| LAB 2 | варианты использования | `Przypadki Uzycia/przypadki_uzycia.md` (v1), исправлено в `przypadki_uzycia_v2.md` (16.11) |
| LAB 3 | список и диаграмма классов | `docs/05_lista_klas.pdf` |
| LAB 4 | UML → Python, первые классы | [LAB4.md](LAB4.md) |
| LAB 5 | проверки, ошибки, наследование | [LAB5.md](LAB5.md) |
| LAB 6 | модель данных и SQLite | [LAB6.md](LAB6.md) |
| LAB 7 | первое окно (Tkinter) | [LAB7.md](LAB7.md) |

## Git

Коммиты делаешь сам:

```bash
git add .
git commit -m "LAB N: opis zmian"
git push
```

Папки `.files/` и `data/` в репозиторий не попадают (они в `.gitignore`).

## Полезное в VS Code

| Действие | Клавиши |
|---|---|
| Перейти к коду метода | Cmd + клик (или F12) |
| Вернуться назад | Ctrl + - |
| Открыть файл по имени | Cmd + P |
| Перейти на строку | Ctrl + G |
| Перечитать файл с диска | Cmd + Shift + P → «File: Revert File» |
