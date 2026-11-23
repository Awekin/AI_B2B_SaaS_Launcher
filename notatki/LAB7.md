# LAB 7. Первый графический интерфейс (Tkinter)

## 1. Что требовалось

Цель со слайдов: пользователь больше не работает с программой через меню в терминале, а пользуется настоящим окном.

| Требование (слайд «Co ma być gotowe po LAB 7?») | Как выполнено |
|---|---|
| 1. Главное окно со своим заголовком и понятной раскладкой | окно «AI B2B SaaS Launcher» 700×450: форма сверху, кнопки, таблица, строка статуса |
| 2. Виджеты: минимум Label, Entry, Button и элемент для показа данных | `Label`, `Entry`, `Combobox`, `Button`, `Frame`, `Treeview` (таблица) |
| 3. События: минимум одно действие пользователя вызывает метод программы | 2 кнопки, у каждой `command=` → метод |
| 4. GUI в отдельном файле или классе, а не всё в `main.py` | класс `MainWindow` в `src/gui/main_window.py` |
| 5. Кнопка запускает существующую функцию приложения | «Utwórz modpack» → `ModpackManager.create_modpack` (UC01), «Usuń zaznaczony» → `ModpackManager.delete_modpack` (UC02) |

По слайдам подключать базу полностью не обязательно. У нас она подключилась сама: окно вызывает `ModpackManager`, а он ещё на LAB 6 сохранял всё в SQLite.

## 2. Что изменилось

| Файл | Что |
|---|---|
| `src/gui/main_window.py` | **новый**, класс `MainWindow`: всё окно |
| `src/gui/__init__.py` | **новый**, чтобы писать `from gui import MainWindow` |
| `src/main.py` | теперь только запускает: менеджер → база → окно |
| `src/console_menu.py` | бывший `main.py` с LAB 6 (меню в терминале), оставлен для тестов |

Классы из `models/` (Mod, Modpack, ModpackManager, Database) **не менялись**. Именно это и требует слайд «GUI powinno być częścią architektury».

## 3. Как это устроено (главная идея)

```
Пользователь → клик → command= → метод MainWindow → ModpackManager → Database → SQLite
   (окно)                         (gui/)              (logika, models/)   (dane)
```

- **GUI** (`MainWindow`) только берёт текст из полей и показывает результат. Своих проверок и SQL в нём нет.
- **Логика** (`ModpackManager`, `Modpack`) проверяет данные и бросает ошибки, как на LAB 5.
- **Данные** (`Database`) пишет в SQLite, как на LAB 6.

Поэтому ошибки (пустое имя, дубликат, плохая версия) окно не проверяет само. Оно ловит `LauncherError` из логики и показывает его текст в окошке.

## 4. Код по строкам

### `src/main.py`

| Строка | Что делает |
|---|---|
| 16 | создаёт `ModpackManager`, он открывает базу |
| 17 | `manager.load()` читает модпаки из базы |
| 19 | `tk.Tk()` создаёт главное окно |
| 20 | `MainWindow(root, manager)` строит в окне виджеты и передаёт ему менеджера |
| 21 | `root.mainloop()` держит окно открытым и ждёт событий (кликов) |
| 23 | после закрытия окна закрывает базу |

### `src/gui/main_window.py`

| Строки | Что делает |
|---|---|
| 14–21 | `__init__`: запоминает `root` и `manager`, ставит заголовок и размер, вызывает `create_widgets()` и `refresh_list()` |
| 23–67 | `create_widgets`: строит окно |
| 25 | `Frame`, группа для полей формы |
| 28–41 | `Label` + `Entry` для названия и версии, `Combobox` для загрузчика |
| 46 | кнопка «Utwórz modpack», `command=self.create_modpack` |
| 47 | кнопка «Usuń zaznaczony», `command=self.delete_modpack` |
| 51–63 | `Treeview`, таблица модпаков (место для показа данных) и ширина колонок |
| 66 | `Label` внизу для сообщений |
| 70–81 | `refresh_list`: очищает таблицу и заново заполняет её из `manager.modpacks` |
| 84–99 | `create_modpack` (UC01): `entry.get()` → `manager.create_modpack(...)` → ошибка в окошке или обновление таблицы |
| 102–113 | `delete_modpack` (UC02): берёт выделенную строку → спрашивает «точно?» → `manager.delete_modpack(id)` → обновляет таблицу |

Хитрость в строке 75: `iid=pack.id`. Номером строки в таблице служит id модпака, поэтому при удалении сразу известно, какой модпак удалять.

## 5. Запуск

```bash
cd "/Users/awekin/Files/PK/Technologie obiektowe - Projekt/AI B2B SaaS Launcher"
python3 src/main.py
```

**Важно про Mac.** Системный `python3` (3.9 от Apple) идёт со старым Tk 8.5. На новой macOS окно с ним зависает и не рисуется. Нужен Python с Tk 8.6 или новее. Самый простой способ:

```bash
brew install python-tk@3.13
python3.13 src/main.py
```

Проверить версию Tk: `python3.13 -c "import tkinter; print(tkinter.TkVersion)"` должно показать 8.6 или 9.0.

Старое меню в терминале (LAB 6) по-прежнему работает: `python3 src/console_menu.py`.

## 6. Сценарий показа преподавателю

1. Запустить `python3.13 src/main.py`. Откроется окно, в таблице модпаки из базы.
   *„To jest główne okno aplikacji. Tytuł ustawiam w `__init__`, a widgety tworzy metoda `create_widgets`.”*
2. Показать виджеты.
   *„Mam Label i Entry na nazwę i wersję, Combobox na loader, dwa przyciski i Treeview, czyli tabelę z danymi.”*
3. Ввести название, например `Test`, нажать **Utwórz modpack**. Строка появится в таблице.
   *„Przycisk ma `command=self.create_modpack`. Metoda bierze tekst z Entry przez `get()` i woła `manager.create_modpack`, czyli tę samą metodę co na LAB 5 i 6. Modpack od razu jest w bazie.”*
4. Ещё раз нажать с тем же названием → окно с ошибкой «już istnieje».
   *„Okno samo nie sprawdza danych. Błąd rzuca logika, a okno tylko go pokazuje.”*
5. Выделить строку и нажать **Usuń zaznaczony** → «Tak».
   *„Drugi przycisk woła `manager.delete_modpack`.”*
6. Открыть `src/gui/main_window.py` и `src/main.py`.
   *„GUI jest w osobnym pakiecie `gui`, w klasie `MainWindow`. `main.py` tylko uruchamia aplikację.”*

## 7. Вопросы преподавателя

**«Co dzieje się po kliknięciu tego przycisku?»**
*„Tkinter wywołuje metodę podaną w `command=`, czyli `create_modpack`. Ona pobiera dane z pól przez `get()`, woła `ModpackManager.create_modpack`, a ten sprawdza dane i zapisuje modpack w SQLite. Na koniec okno odświeża tabelę albo pokazuje błąd.”*

**«Gdzie znajduje się metoda, którą właśnie uruchomiłeś?»**
*„Obsługa kliknięcia jest w `src/gui/main_window.py`, metoda `MainWindow.create_modpack`. Właściwa logika jest w `src/models/modpack_manager.py`, metoda `create_modpack`.”*

**«Jak GUI będzie połączone z logiką i SQLite?»**
*„Już jest połączone przez `ModpackManager`. Okno dostaje menedżera w konstruktorze i woła tylko jego metody. Kierunek jest taki: interfejs → logika → dane. GUI nie pisze SQL.”*

**«Co robi `mainloop()`?»**
*„Trzyma okno otwarte i czeka na zdarzenia użytkownika, na przykład kliknięcia.”*

**«Czym jest ttk?»**
*„To nowocześniejsze widgety Tkintera, wyglądają jak systemowe.”*

**«Dlaczego GUI w osobnej klasie?»**
*„Żeby nie mieszać wyglądu z logiką. Klasy modelu się nie zmieniły, a okno można później wymienić.”*

## 8. Словарик

| Слово | Что это |
|---|---|
| Tkinter | встроенная в Python библиотека для окон |
| ttk | более современные виджеты Tkinter |
| виджет | элемент окна: надпись, поле, кнопка, таблица |
| `Label` | надпись |
| `Entry` | поле для ввода текста |
| `Button` | кнопка |
| `Combobox` | выпадающий список |
| `Frame` | рамка, группирует виджеты |
| `Treeview` | таблица со строками |
| `messagebox` | всплывающее окошко (ошибка, вопрос) |
| `command=` | какой метод вызвать при клике |
| `mainloop()` | цикл, который держит окно и ждёт событий |
| событие | действие пользователя (клик, ввод) |
| `pack` / `grid` | способы расставить виджеты: друг за другом или по сетке |
