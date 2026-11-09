# LAB 5. Логика объектов: проверки, ошибки, наследование

## 1. Что требовалось

**Тема:** «model zaczyna zachowywać się jak aplikacja». Интерфейс пока не делаем.

**Цель:** довести минимум 2–3 варианта использования (UC) до реальной работы и защитить их от основных ошибочных данных.

**Что показать преподавателю** (слайд «Zanim wyjdziesz – pokaż mi LAB 5»):

| Требование | Что показываем |
|---|---|
| Выбранный UC из документации | UC01, UC04 (вместе с UC03) из `przypadki_uzycia.md` |
| Запуск функции | `python3 src/main.py` |
| Классы и методы, которые её делают | таблица в разделе 4 |
| Пример ошибочных данных / проверки | блоки «błędne dane» в выводе |
| Актуальная диаграмма UML | `docs/06_diagram_klas_v2.drawio` (+ PNG) |

**Принцип оценки:** «Odbiór = działanie + rozumienie kodu» — работает и ты понимаешь код.

**Наследование** — только если проходит проверку «X **JEST** Y». Не добавлять «bo UML wygląda bardziej obiektowo».

**Дальше (LAB 6):** сохранение данных в SQLite.

## 2. Что изменилось по сравнению с LAB 4

```
src/models/
  exceptions.py          НОВЫЙ  свои классы ошибок
  validation.py          НОВЫЙ  общие проверки данных
  mod.py                 проверки в конструкторе
  modpack.py             проверки в конструкторе + 3 проверки в add_mod + ошибки в remove/toggle
  modpack_manager.py     проверка уникальности названия + ошибка при удалении
src/main.py              показывает правильные и ошибочные данные
```

Идея простая: **раньше программа принимала любые данные, теперь она отказывается работать с неправильными и объясняет почему.**

## 3. Новые файлы — простыми словами

### exceptions.py — свои ошибки
Ошибка (исключение) — это способ сказать «стоп, так нельзя». `raise` выбрасывает ошибку, `try / except` её ловит.

Вместо одной общей ошибки у нас 6 своих, чтобы было понятно, **что именно** пошло не так:

| Класс | Когда возникает |
|---|---|
| `LauncherError` | общий «родитель» всех наших ошибок |
| `ValidationError` | плохие данные: пустое поле, неизвестный загрузчик, плохая версия игры |
| `DuplicateError` | такое уже есть: модпак с таким названием или мод в модпаке |
| `NotFoundError` | такого нет: мода или модпака с таким id |
| `IncompatibleModError` | мод не подходит к версии игры или загрузчику |
| `ModConflictError` | мод конфликтует с модом, который уже в модпаке |

**Наследование:** все 5 ошибок наследуются от `LauncherError` (`class ValidationError(LauncherError)`). Проверка со слайда проходит: «ValidationError JEST błędem launchera».
Польза: в `main.py` ловим только `except LauncherError`, а перехватываются **все** 5 видов ошибок.

### validation.py — общие проверки
Три функции, которые используют и `Mod`, и `Modpack` (чтобы не писать одно и то же дважды):
- `require_text` — поле не пустое и не из одних пробелов;
- `validate_loader` — загрузчик один из: fabric, forge, neoforge, quilt;
- `validate_game_version` — версия похожа на `1.20` или `1.20.1`.

Если проверка не прошла — `raise ValidationError(...)`.

## 4. Варианты использования и классы

### UC01 — Utwórz modpack
**Классы:** `ModpackManager`, `Modpack`.

| Где | Что проверяется | Ошибка | Сценарий в документации |
|---|---|---|---|
| `Modpack.__init__` (modpack.py:21) | название не пустое, ≤ 50 символов | `ValidationError` | 3b |
| `Modpack.__init__` | версия игры в формате 1.20.1 | `ValidationError` | 3b |
| `Modpack.__init__` | загрузчик из списка | `ValidationError` | 3b |
| `create_modpack` (modpack_manager.py:22) | нет модпака с таким названием | `DuplicateError` | 3a |

### UC04 — Zarządzaj modami (+ UC03 — Sprawdź kompatybilność)
**Классы:** `Modpack`, `Mod`. UC03 входит в UC04 через «include» на диаграмме UC.

| Где | Что проверяется | Ошибка |
|---|---|---|
| `Mod.__init__` (mod.py:11) | id, название, версия не пустые; версия игры и загрузчик правильные | `ValidationError` |
| `add_mod` шаг 1 (modpack.py:46) | мода ещё нет в модпаке | `DuplicateError` |
| `add_mod` шаг 2 (modpack.py:49) | мод подходит по версии и загрузчику — спрашиваем `mod.is_compatible` | `IncompatibleModError` |
| `add_mod` шаг 3 (modpack.py:54) | **UC03:** мод не конфликтует ни с одним модом — спрашиваем `mod.conflicts_with` | `ModConflictError` (сценарий 5a) |
| `remove_mod` / `toggle_mod` | такой мод есть в модпаке | `NotFoundError` |

**Współpraca obiektów:** модпак не решает сам, подходит ли мод, — он спрашивает сам мод (`is_compatible`, `conflicts_with`).

## 5. Что выводит программа

```
== UC01: błędne dane ==
  Odrzucono [ValidationError]: Pole 'nazwa modpacka' nie może być puste.
  Odrzucono [DuplicateError]: Modpack o nazwie 'optymalizacja' już istnieje. Podaj inną nazwę.
  Odrzucono [ValidationError]: Nieznany loader 'minecraft'. Dozwolone: fabric, forge, neoforge, quilt.
  Odrzucono [ValidationError]: Niepoprawna wersja gry 'najnowsza'. Oczekiwany format np. 1.20.1.
  Liczba modpacków po błędach: 1          ← после 4 ошибок модпак по-прежнему один

== UC04 + UC03: błędne dane ==
  Odrzucono [DuplicateError]: Mod 'Sodium' jest już w modpacku 'Optymalizacja'.
  Odrzucono [IncompatibleModError]: Mod 'Create' nie pasuje do modpacka (fabric 1.20.1).
  Odrzucono [ModConflictError]: Mod 'OptiFabric' koliduje z modem 'Sodium'.
  Odrzucono [ValidationError]: Pole 'id moda' nie może być puste.
  Odrzucono [NotFoundError]: W modpacku 'Optymalizacja' nie ma moda o id 'jei'.

== UC04: wyłączenie moda ==
  Aktywne mody: Fabric API, Sodium
  Stan modpacka: Modpack(Optymalizacja, fabric 1.20.1, modów: 3)   ← после ошибок модпак цел
```

В квадратных скобках — название класса ошибки, чтобы было видно, какая проверка сработала.
Важно: **программа не падает**, а после всех ошибок данные остаются правильными (1 модпак, 3 мода).

## 6. Сценарий показа (≈ 5 минут)

1. **Назвать UC.** «Pokażę UC01 — tworzenie modpacka i UC04 — zarządzanie modami, razem z UC03 — sprawdzeniem kompatybilności. Są w dokumentacji z LAB 2.»
2. **Запустить** `python3 src/main.py`.
3. **UC01, правильные данные:** Cmd + клик на `create_modpack` → «menedżer tworzy modpack, konstruktor Modpack sprawdza dane».
4. **UC01, ошибки:** показать 4 строки «Odrzucono». Cmd + клик на `Modpack(` → `__init__` → «tu jest walidacja danych: `require_text`, `validate_game_version`, `validate_loader`». Cmd + клик на `validate_loader` → показать проверку.
5. **UC04, ошибки:** Cmd + клик на `add_mod` → «trzy sprawdzenia: duplikat, wersja i loader, konflikt z innymi modami. Jeśli któreś nie przejdzie — mod nie jest dodany».
6. **Ошибки:** открыть `exceptions.py` → «własne wyjątki, wszystkie dziedziczą po LauncherError, dlatego w main.py łapiemy je jednym `except LauncherError`».
7. **Итог:** последняя строка вывода → «po wszystkich błędach modpack jest dalej poprawny».
8. **Диаграмма v2:** «dodaliśmy hierarchię wyjątków — model się zmienił, więc diagram też».

## 7. Контрольные вопросы

| Вопрос | Ответ |
|---|---|
| Który Use Case właśnie pokazałeś? | UC01 — tworzenie modpacka i UC04 — zarządzanie modami, razem z UC03 — sprawdzeniem kompatybilności, które jest w UC04 przez «include». |
| Które klasy za niego odpowiadają? | UC01: ModpackManager i Modpack. UC04 i UC03: Modpack i Mod. Błędy są w exceptions.py. |
| Gdzie jest walidacja? | Na dwóch poziomach. Dane — w konstruktorach Mod i Modpack, przez funkcje z validation.py. Reguły — w metodach: add_mod, remove_mod, toggle_mod, create_modpack. |
| Co stanie się przy błędnych danych? | Rzucany jest wyjątek, main.py go łapie i wypisuje komunikat. Obiekt nie powstaje albo modpack zostaje bez zmian — program się nie wysypuje. |
| Gdzie jest dziedziczenie? | W wyjątkach: każdy błąd dziedziczy po LauncherError, bo JEST błędem launchera. W klasach modelu nie dodawaliśmy dziedziczenia na siłę. |
| Dlaczego nie ma dziedziczenia w modelu? | Żadna klasa nie jest rodzajem innej. Może pojawić się później, np. różne loadery, jeśli uruchamianie gry będzie się różnić. |
| Dlaczego własne wyjątki, a nie ValueError? | Z nazwy widać, co poszło nie tak, i można je łapać wszystkie naraz przez LauncherError. |
| Co to jest `raise`? | Zgłoszenie błędu — przerywa metodę. |
| Co to jest `try / except`? | Próbujemy wykonać kod; jeśli pojawi się błąd, łapiemy go i obsługujemy zamiast wysypać program. |
| Dlaczego walidacja w konstruktorze? | Żeby niepoprawny obiekt w ogóle nie powstał. |
| Czy model się zmienił? | Tak — doszły klasy wyjątków, dlatego jest diagram v2. Klasy modelu i ich metody się nie zmieniły. |

## 8. Новые слова Python

| Термин | Что это |
|---|---|
| `raise X("...")` | выбросить ошибку X с сообщением |
| `try: ... except X as error:` | поймать ошибку X и сохранить её в переменную `error` |
| `class B(A):` | класс B наследуется от A (B **является** A) |
| `pass` | «ничего не делать» — класс без собственного кода |
| `isinstance(x, str)` | проверка, что x — текст |
| `.strip()` | убрать пробелы по краям |
| `.lower()` | перевести в маленькие буквы |
| `re` / `fullmatch` | проверка текста по шаблону (у нас — формат версии 1.20.1) |
| `any(...)` | «есть ли хотя бы один такой» |
| `type(error).__name__` | название класса ошибки — так в выводе появляется `[ValidationError]` |
