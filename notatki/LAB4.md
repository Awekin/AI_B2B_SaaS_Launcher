# LAB 4. UML → Python, первая реализация

> Состояние кода на момент сдачи LAB 4 — коммит `be9cfe4` («LAB 4: klasy z diagramu UML i main.py»).
> На LAB 5 код дополнен проверками и ошибками, поэтому номера строк сейчас другие.

## 1. Что требовалось

Слайд «Co ma być gotowe po LAB 4?»:

| № | Требование | Как выполнено |
|---|---|---|
| 1 | Проект Python: папка `src/` + `main.py` | `src/main.py`, `src/models/` |
| 2 | Минимум 3 класса по диаграмме UML | `Mod`, `Modpack`, `ModpackManager` |
| 3 | `__init__` и атрибуты из UML | у всех трёх классов |
| 4 | Минимум одна связь между объектами | композиция и ассоциация |
| 5 | `main.py` показывает хотя бы одну функцию | UC01 и UC04 |

Главный принцип лабы: **«nie projektujemy od zera — kodujemy UML»** — ничего не придумываем, переносим диаграмму в код.

## 2. Структура проекта

```
src/
  main.py                 запуск и демонстрация
  models/
    __init__.py           собирает классы в один пакет
    mod.py                класс Mod
    modpack.py            класс Modpack
    modpack_manager.py    класс ModpackManager
```

Один класс — один файл. Слайд прямо называет плохим примером «вся программа в одном огромном main.py».

Из 6 классов диаграммы реализованы 3. `ModRepository`, `ModResolver`, `GameLauncher` работают с интернетом и серверами Microsoft — их добавим позже.

## 3. Классы

### Mod — один мод
- Атрибуты: id, название, версия, версия игры, загрузчик, зависимости, конфликты, имя файла.
- `is_compatible(game_version, loader)` — подходит ли мод к версии игры и загрузчику.
- `conflicts_with(other)` — конфликтует ли с другим модом.

### Modpack — набор модов
- Атрибуты: id, название, версия игры, загрузчик, список модов, выключенные моды, дата создания.
- `add_mod` — добавляет мод (с ошибкой, если мод уже есть или не подходит).
- `remove_mod` — удаляет мод.
- `toggle_mod` — включает/выключает мод, не удаляя его.
- `get_active_mods` — только включённые моды.

### ModpackManager — хранилище модпаков
- Атрибуты: список модпаков, папка с данными.
- `create_modpack` — создаёт новый модпак с уникальным id (`uuid`).
- `delete_modpack` — удаляет модпак.

## 4. Связи

| Связь | Где в коде | Как объяснить |
|---|---|---|
| Композиция `ModpackManager ◆— Modpack` | `self._modpacks = []` в менеджере | менеджер **сам создаёт** модпаки, без него они не существуют |
| Ассоциация `Modpack — Mod` | `self._mods = []` в модпаке | модпак **хранит ссылки** на моды, но не создаёт их; один мод может быть в нескольких модпаках |

## 5. Сценарий показа

1. Запустить `python3 src/main.py`, показать вывод.
2. Пройти по `main.py` сверху вниз, на каждом вызове **Cmd + клик** → показать код метода → **Ctrl + -** назад.
3. Порядок: `ModpackManager` → `create_modpack` → `Modpack.__init__` → `Mod.__init__` → `add_mod` → `is_compatible` → `toggle_mod` → `get_active_mods`.
4. Итог: «aktywne 2, a modów 3 — wyłączenie nie usuwa moda».

Цепочка для памяти: **менеджер создаёт модпак → модпак хранит моды → мод сам проверяет, подходит ли он.**

## 6. Вопросы и ответы

| Вопрос | Ответ |
|---|---|
| Czy struktura plików odpowiada diagramowi? | Tak, każda klasa ma osobny plik w `src/models/`. Zaimplementowaliśmy 3 z 6 klas, pozostałe dodamy na kolejnych etapach. |
| Gdzie jest relacja? | `self._modpacks` w ModpackManager — kompozycja; `self._mods` w Modpack — asocjacja. |
| Co to jest `self`? | Referencja do bieżącego obiektu. |
| Co to jest `__init__`? | Konstruktor — wywołuje się przy tworzeniu obiektu i ustawia atrybuty. |
| Dlaczego `_` przed atrybutami? | To atrybuty prywatne, minus na diagramie. Do odczytu jest `@property`. |
| Co to `__repr__`? | Jak obiekt wygląda po `print`. |
| Skąd `uuid`? | Generuje unikalne id modpacka. |

## 7. Мини-словарь Python

| Термин | Что это |
|---|---|
| `class X:` | объявление класса (шаблон объектов) |
| объект | конкретный экземпляр класса |
| `def` | функция / метод |
| `self` | «этот объект» |
| `__init__` | конструктор |
| `[]` | пустой список |
| `set()` | множество — список без повторов |
| `@property` | позволяет прочитать приватное поле, но не изменить |
| `try / except` | «попробуй; если ошибка — сделай вот это» |
| `raise` | выбросить ошибку |
| `import` | подключить код из другого файла |
| `#` | комментарий, Python его не выполняет |
