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

**Предполагаемый стек:** PySide6 (интерфейс), `minecraft-launcher-lib` (установка и запуск игры, вход Microsoft), PyInstaller (сборка `.app`).

## Где что лежит

```
Technologie obiektowe - Projekt/
  AI B2B SaaS Launcher/        приложение (git-репозиторий)
    src/main.py                запуск и демонстрация
    src/models/                классы из диаграммы
    notatki/                   эти заметки
  docs/                        список классов (PDF), диаграммы классов v1, v2
  Przypadki Uzycia/            варианты использования (LAB 2)
  archiwum/lab4_pelna_wersja/  полная версия с 6 классами и Modrinth (на будущее)
```

## Классы

| Класс | Что делает | Статус |
|---|---|---|
| `Mod` | один мод | готов |
| `Modpack` | набор модов для одной версии игры и загрузчика | готов |
| `ModpackManager` | хранит, создаёт и удаляет модпаки | частично (нет импорта/экспорта, копий, сохранения) |
| `ModRepository` | поиск и скачивание модов из Modrinth | позже (есть в архиве) |
| `ModResolver` | зависимости и конфликты | позже (есть в архиве) |
| `GameLauncher` | вход Microsoft и запуск игры | позже |
| ошибки в `exceptions.py` | свои исключения, все от `LauncherError` | готовы (LAB 5) |

## Варианты использования (из LAB 2)

| UC | Название | В коде |
|---|---|---|
| UC01 | Utwórz modpack | ✔ |
| UC02 | Rozwiąż zależności | позже |
| UC03 | Sprawdź kompatybilność | ✔ (конфликты в `add_mod`) |
| UC04 | Zarządzaj modami | ✔ |
| UC05 | Zarządzaj kopiami zapasowymi | позже |
| UC06 | Importuj modpack | позже |
| UC07 | Eksportuj modpack | позже |
| UC08 | Uruchom Minecraft | позже |
| UC09 | Przeglądaj katalog modów | позже |

## Лабы

| Лаба | Тема | Заметки |
|---|---|---|
| LAB 2 | варианты использования | `Przypadki Uzycia/przypadki_uzycia.md` |
| LAB 3 | список и диаграмма классов | `docs/05_lista_klas.pdf` |
| LAB 4 | UML → Python, первые классы | [LAB4.md](LAB4.md) |
| LAB 5 | проверки, ошибки, наследование | [LAB5.md](LAB5.md) |
| LAB 6 | сохранение данных в SQLite | будет |

## Git

Коммиты делаешь сам:

```bash
git add .
git commit -m "LAB N: opis zmian"
git push
```

Папка `.files/` в репозитории не попадает (она в `.gitignore`).

## Полезное в VS Code

| Действие | Клавиши |
|---|---|
| Перейти к коду метода | Cmd + клик (или F12) |
| Вернуться назад | Ctrl + - |
| Открыть файл по имени | Cmd + P |
| Перейти на строку | Ctrl + G |
| Перечитать файл с диска | Cmd + Shift + P → «File: Revert File» |
