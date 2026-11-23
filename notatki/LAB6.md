# LAB 6. Модель данных и SQLite

## 1. Что требовалось

**Тема:** «LAB 5: aplikacja działa → LAB 6: aplikacja działa i pamięta». Раньше после закрытия программы все модпаки пропадали. Теперь они сохраняются в базу SQLite.

**Что показать преподавателю** (слайд «Co powinno być gotowe po LAB 6»):

| Требование | Что показываем |
|---|---|
| Модель данных / таблицы | `docs/07_model_danych.png` и раздел 3 ниже |
| Файл database.db | `data/database.db` (появляется после первого запуска) |
| Код соединения с SQLite | `src/models/database.py`, класс `Database` |
| Запись данных | `Database.save_modpack` (INSERT) |
| Чтение данных | `Database.load_modpacks` (SELECT) |
| Данные остаются после перезапуска | тест из раздела 5 |

**Минимум со слайда «Zadanie 2»:** создать базу и таблицы, записать один тип данных, прочитать его, хотя бы одна функция работает через базу, **значения передаём через параметры `?`, а не склеиваем строку SQL**. Всё выполнено.

**Принцип оценки:** «Odbiór = działanie + trwałość danych» — работает и данные не теряются.

Интерфейс не нужен («Bez GUI»), поэтому в консоли простое текстовое меню.

## 2. Что изменилось по сравнению с LAB 5

```
src/models/
  database.py            НОВЫЙ  класс Database: вся работа с SQLite
  modpack_manager.py     открывает базу, create/delete сразу пишут в базу, появились save(), load(), close()
  modpack.py             можно передать дату создания (при чтении из базы), свойства для чтения, is_enabled()
  mod.py                 свойства для чтения всех полей (базе нужно их прочитать)
src/main.py              текстовое меню вместо демонстрации
data/database.db         файл базы (создаётся сам, в git не попадает)
.gitignore               добавлена папка /data/
```

Логика модпаков и проверки из LAB 5 **не менялись**: все ошибки работают как раньше.

## 3. Модель данных (Zadanie 1)

**Какие данные должны пережить перезапуск:** модпаки (название, версия игры, загрузчик, дата создания) и моды в каждом модпаке, включая информацию, включён мод или выключен.

Две таблицы, как просит слайд («minimum 1–2 tabele»):

```
modpacks                              mods
  id            TEXT  PK  ◄────┐        id                INTEGER PK
  name          TEXT  UNIQUE   └──────  modpack_id        TEXT    FK → modpacks.id
  game_version  TEXT                    mod_id            TEXT    (например "sodium")
  loader        TEXT                    name, version     TEXT
  created_at    TEXT                    game_version      TEXT
                                        loader            TEXT
                                        dependencies      TEXT    (id через запятую)
                                        incompatible_with TEXT    (id через запятую)
                                        file_name         TEXT
                                        enabled           INTEGER (1 / 0)
```

Картинка: `docs/07_model_danych.png`.

### Класс → таблица (слайд «Model danych: klasa → tabela»)

| Атрибут в Python | Куда попадает в базе |
|---|---|
| `Modpack._id`, `_name`, `_game_version`, `_loader` | столбцы таблицы `modpacks` с теми же названиями |
| `Modpack._created_at` (datetime) | `modpacks.created_at`, текст вида `2026-11-16T18:19:00` |
| `Modpack._mods` (список модов) | строки в таблице `mods` с `modpack_id` этого модпака, это **FK** |
| `Modpack._disabled_mods` (множество id) | столбец `mods.enabled`: 0 = выключен |
| `Mod._id` | `mods.mod_id` |
| `Mod._name`, `_version`, `_game_version`, `_loader`, `_file_name` | столбцы `mods` с теми же названиями |
| `Mod._dependencies`, `_incompatible_with` (списки) | текст через запятую: `"sodium,lithium"` |

### Почему именно так (если спросят)

- **Связь Modpack — Mod записана через FK** `mods.modpack_id`. Слайд: «Relacje obiektowe w bazie często zapisujemy przez identyfikatory (klucze obce)».
- **`ON DELETE CASCADE`**: при удалении модпака его моды удаляются сами.
- **`mods.id` — отдельный INTEGER PK**, потому что один и тот же мод (например sodium) может лежать в двух модпаках. Поэтому `mod_id` сам по себе не уникален, уникальна пара `(modpack_id, mod_id)`.
- **Списки хранятся текстом через запятую.** Для них можно было сделать ещё 2 таблицы, но слайд говорит «Projektuj tylko to, czego naprawdę potrzebuje aplikacja». Id модов запятых не содержат.
- **Выключенные моды — не отдельная таблица, а столбец `enabled`**: это свойство мода внутри конкретного модпака.
- **`id` модпака — TEXT**, потому что это uuid, его создаёт программа, а не база.

## 4. Код — простыми словами

### database.py — класс Database (Zadanie 2)
Весь SQL лежит только здесь, остальная программа SQL не пишет.

| Метод | Что делает | SQL |
|---|---|---|
| `__init__` (database.py:45) | `sqlite3.connect` открывает или создаёт файл, включает внешние ключи | `PRAGMA foreign_keys = ON` |
| `create_tables` (database.py:58) | создаёт таблицы, если их ещё нет | `CREATE TABLE IF NOT EXISTS` |
| `save_modpack` (database.py:67) | **запись**: удаляет старую версию модпака и записывает актуальную вместе с модами, потом `commit()` | `DELETE`, `INSERT ... VALUES (?, ?, ...)` |
| `delete_modpack` (database.py:106) | удаляет модпак, моды удаляются каскадом | `DELETE ... WHERE id = ?` |
| `load_modpacks` (database.py:113) | **чтение**: из строк базы заново создаёт объекты `Modpack` и `Mod` | `SELECT ... FROM modpacks`, потом `SELECT ... FROM mods WHERE modpack_id = ?` |
| `close` (database.py:151) | закрывает соединение | |

Те же шаги, что на слайде «Pierwsze połączenie z bazą»: `connect()` → `cursor()` → `execute(CREATE TABLE ...)` → `commit()` → `close()`.

**Важное при чтении:** объекты создаются через обычные конструкторы и `add_mod`, поэтому проверки из LAB 5 работают и для данных из базы. Испорченная запись (например, кто-то вручную вписал loader = "minecraft") пропускается с сообщением, программа не падает.

**Знаки `?`**: значения не вклеиваются в текст SQL, их подставляет сама SQLite. Так требует слайд («brak konkatenowania wartości, używamy parametrów»), и это защита от SQL injection.

**`rollback()`**: если при записи модпака что-то сломалось, база остаётся как была (транзакция).

### modpack_manager.py — связь логики с базой

| Метод | Что делает с базой |
|---|---|
| `__init__` (:14) | создаёт папку `data` и объект `Database` (композиция: менеджер владеет базой) |
| `create_modpack` (:31) | **UC01** — после проверок пишет новый модпак в базу |
| `delete_modpack` (:42) | **UC02** — удаляет из базы |
| `save` (:49) | записывает все модпаки, вызываем после изменения модов (UC04, UC06) |
| `load` (:54) | читает все модпаки при старте программы |
| `close` (:58) | закрывает базу |

Методы `save()` и `load()` **уже были на диаграмме классов с самого начала**, теперь они реализованы. Новый класс `Database` добавлен на диаграмму классов v3.

### main.py — меню

```
1 - pokaż modpacki
2 - utwórz modpack (UC01)
3 - usuń modpack (UC02)
4 - włącz / wyłącz mod (UC06)
5 - dodaj przykładowe dane (UC01 + UC04)
0 - wyjście
```

При запуске программа сразу читает базу и показывает, что в ней лежит.

## 5. Главный тест (слайд «Najważniejszy test LAB 6»)

Перед показом удалить старую базу, чтобы начать с пустой:

```bash
rm -f data/database.db
```

| Шаг | Что делаешь | Что видно |
|---|---|---|
| 1. Uruchom program | `python3 src/main.py` | «Liczba modpacków: 0», «Baza jest pusta» — **пустая база** |
| 2. Dodaj dane | `5`, потом `2` и свой модпак, например `Survival`, `1.21.1`, `neoforge` | 2 примера + твой — **несколько записей**; OptiFabric отклонён (конфликт) |
| 2a. Błędne dane | `2`, название `optymalizacja` | «Odrzucono [DuplicateError]» — **ошибочные данные** не попадают в базу |
| 2b. | `4`, выключить мод (например Lithium) | «zapisano w bazie» |
| 3. Zamknij program | `0` | «Koniec. Dane zostały w bazie…» |
| 4. Uruchom ponownie | `python3 src/main.py` | |
| 5. Pokaż te same dane | — | те же модпаки, моды и **тот же статус «wyłączony»** |

«Dane po restarcie = główny cel LAB 6 osiągnięty.»

Можно ещё показать, что файл реально существует:

```bash
ls -l data/
sqlite3 data/database.db "SELECT name, loader FROM modpacks;"
```

## 6. Сценарий показа (≈ 5 минут)

1. **Проблема.** «Na LAB 5 aplikacja działała, ale po zamknięciu dane znikały. Teraz zapisujemy je w SQLite.»
2. **Модель данных.** Открыть `docs/07_model_danych.png`. «Dwie tabele: `modpacks` i `mods`. Relacja Modpack–Mod jest zapisana kluczem obcym `modpack_id`.»
3. **Тест с перезапуском** — раздел 5.
4. **Код.** Открыть `database.py`:
   - `__init__` → «`connect` otwiera albo tworzy plik database.db»;
   - `create_tables` → «`CREATE TABLE IF NOT EXISTS`, tabele powstają tylko za pierwszym razem»;
   - `save_modpack` → «zapis: `INSERT` z parametrami `?`, nie sklejamy SQL, na końcu `commit`»;
   - `load_modpacks` → «odczyt: `SELECT`, z wierszy tworzymy z powrotem obiekty Modpack i Mod, przez te same konstruktory, więc walidacja z LAB 5 też działa».
5. **Связь с логикой.** `modpack_manager.py` → `create_modpack` → «UC01 po walidacji od razu zapisuje do bazy».
6. **UML.** `docs/06_diagram_klas_v3.drawio` → «doszła klasa Database, ModpackManager ją posiada (kompozycja), metody save i load były na diagramie od początku».

## 7. Контрольные вопросы

| Вопрос | Ответ |
|---|---|
| Który obiekt z UML zapisujesz w tej tabeli? | W tabeli `modpacks` — obiekty klasy Modpack, jeden wiersz to jeden modpack. W tabeli `mods` — obiekty klasy Mod, razem z informacją, do którego modpacka należą i czy są włączone. |
| Gdzie w bazie trafia konkretny atrybut? | Np. `Modpack.name` → `modpacks.name`. Lista `Modpack.mods` → wiersze w `mods` z kluczem obcym `modpack_id`. Zbiór `disabled_mods` → kolumna `mods.enabled` (0 albo 1). Listy `dependencies` i `incompatible_with` → tekst z id po przecinku. |
| Co się stanie po ponownym uruchomieniu? | `ModpackManager.load()` wywołuje `Database.load_modpacks()`, który robi `SELECT` i odtwarza obiekty Modpack i Mod z danych w bazie. Użytkownik widzi te same modpaki co przed zamknięciem. |
| Który Use Case korzysta już z bazy? | UC01 (tworzenie modpacka — INSERT), UC02 (usuwanie — DELETE), UC04 i UC06 (dodawanie i włączanie/wyłączanie modów — zapis przez `save()`), a przy starcie odczyt wszystkich modpacków (SELECT). |
| Dlaczego SQLite? | Jeden plik bez serwera, moduł `sqlite3` jest wbudowany w Pythona, dobre do aplikacji desktopowej. |
| Jaki jest klucz główny, a jaki obcy? | PK: `modpacks.id` (uuid) i `mods.id`. FK: `mods.modpack_id` → `modpacks.id`. |
| Dlaczego `?` zamiast sklejania tekstu? | Wartości podaje SQLite, więc nie da się „wstrzyknąć” SQL przez dane (SQL injection), a tekst z apostrofem nie zepsuje zapytania. |
| Po co `commit()`? | Bez niego zmiany nie zostaną zapisane w pliku. |
| Co jeśli w bazie są złe dane? | Obiekty są tworzone przez konstruktory z walidacją, więc zły rekord jest pomijany z komunikatem, a program działa dalej. |
| Co z pustą bazą? | Tabele tworzą się automatycznie, program pokazuje „Baza jest pusta” i działa normalnie. |
| Czy model się zmienił? | Doszła klasa Database (diagram v3). Klasy Mod i Modpack dostały tylko metody do odczytu pól, logika się nie zmieniła. |

## 8. Новые слова

| Термин | Что это |
|---|---|
| SQLite | база данных в одном файле, без сервера |
| `sqlite3` | модуль Python для работы с SQLite, уже встроен |
| таблица / строка / столбец | как лист Excel: строка = один объект, столбец = один атрибут |
| PK (primary key) | столбец, по которому строка уникальна |
| FK (foreign key) | столбец со ссылкой на PK другой таблицы, так хранится связь |
| `CREATE TABLE` | создать таблицу |
| `INSERT` / `SELECT` / `DELETE` | добавить / прочитать / удалить строки |
| `cursor` | объект, через который выполняется SQL |
| `commit()` | сохранить изменения в файл |
| `rollback()` | отменить незаписанные изменения |
| `fetchall()` | забрать все найденные строки |
| `ON DELETE CASCADE` | при удалении модпака удалить и его моды |
| `input()` | прочитать то, что пользователь ввёл в консоли |
| `os.path.join` | склеить путь к файлу правильно для системы |
