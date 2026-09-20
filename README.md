# ☕🍵 Кофе и Чай — офлайн-справочник рецептов заваривания

Мобильное приложение на **чистом Python** (Kivy). Работает полностью офлайн:
встроенные рецепты лежат в локальном JSON, избранное, заметки и пользовательские
рецепты — в локальной SQLite-базе.

> В исходном ТЗ упоминались React Native / Flutter, но финальное требование —
> «всё на языке Python». Поэтому стек: **Python 3 + Kivy + SQLite**, сборка APK
> через **Buildozer**. То же приложение запускается на Windows/macOS/Linux
> (для отладки) и собирается под iOS через kivy-ios.

---

## 1. Структура проекта

```
brewbook/
├── main.py                      # точка входа, App, навигация (стек экранов)
├── buildozer.spec               # конфиг сборки APK под Android
├── requirements.txt
├── README.md
└── app/
    ├── __init__.py
    ├── theme.py                 # палитры (тёмная/светлая, карамельные тона)
    ├── i18n.py                  # локализация RU/EN + tr() для словарей рецептов
    ├── units.py                 # граммы↔унции, мл↔fl oz, форматирование
    ├── models.py                # Recipe / Param / Step, пересчёт по порциям
    ├── db.py                    # SQLite: настройки, избранное, заметки, свои рецепты
    ├── utils.py                 # звук, вибрация, «Поделиться», тосты
    ├── widgets.py               # карточки, кнопки, сегментированный переключатель, таймер
    ├── data/
    │   └── recipes.json         # 15 встроенных рецептов (8 кофе + 7 чая)
    └── screens/
        ├── __init__.py
        ├── base.py              # BaseScreen (фон темы, доступ к App)
        ├── home.py              # главный экран: «Кофе» / «Чай» + разделы
        ├── recipe_list.py       # список с вкладками «Базовые» / «Авторские»
        ├── recipe_detail.py     # параметры, шаги, лайфхаки, избранное, заметки
        ├── step_mode.py         # пошаговый режим «поварёнка» с таймерами
        ├── favorites.py         # избранное + «Мои рецепты»
        ├── editor.py            # редактор своих рецептов (+ фото из галереи)
        ├── timers.py            # независимые таймеры (несколько одновременно)
        └── settings.py          # тема, единицы измерения, язык
```

## 2. Запуск на локальной машине

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Окно откроется в «телефонном» формате 420×860. Клавиша **Esc** = кнопка «Назад».

## 3. Сборка APK для Android

```bash
pip install buildozer cython
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config \
     zlib1g-dev libncurses5-dev libtinfo5 cmake libffi-dev libssl-dev

buildozer android debug            # APK появится в bin/
buildozer android debug deploy run logcat   # установить на подключённый телефон
```

Релизная сборка: `buildozer android release` + подпись `apksigner`.

Для iOS: `pip install kivy-ios && toolchain build python3 kivy && toolchain create BrewBook .`

## 4. Что реализовано по ТЗ

| Требование | Где |
|---|---|
| Две категории на старте | `screens/home.py` |
| Вкладки «Базовые» / «Авторские» | `screens/recipe_list.py` |
| Пересчёт граммовок по порциям (1/2 чашки, 1/2/3+ чел.) | `models.Recipe.factor` + `Segmented` |
| Блок «Параметры» (граммовка, вода, молоко, t°, помол, время, давление) | `recipes.json` → `recipe_detail.py` |
| Пошаговый рецепт: номер, название, описание с цифрами, лайфхак | `models.Step`, `recipe_detail._step_card` |
| Режим «поварёнка» с таймером и напоминанием о весах | `screens/step_mode.py` |
| Тея: проливы +5 с кнопкой «Следующий пролив» | `step_mode._next_infusion` |
| Блок «Лайфхаки и тонкости» | поле `tips` в JSON |
| Избранное, заметки, «Поделиться» | `db.py`, `utils.share_text` |
| Редактор своих рецептов + фото из галереи | `screens/editor.py` |
| Независимые таймеры, звук и вибрация | `screens/timers.py`, `utils.py` |
| Тема, единицы измерения, язык | `screens/settings.py` |
| Полный офлайн | JSON + SQLite, сетевых вызовов нет |

## 5. Формат рецепта (recipes.json)

```jsonc
{
  "id": "coffee_espresso",
  "kind": "coffee",            // coffee | tea
  "category": "base",          // base | author
  "name": {"ru": "...", "en": "..."},
  "desc": {"ru": "...", "en": "..."},
  "base_servings": 1,
  "servings_options": [1, 2],
  "params": [
    // value — число или [min, max]; scale=true → умножается на число порций
    {"key": "coffee", "label": {"ru": "Кофе"}, "value": 18, "unit": "g", "scale": true},
    // без value — статический текст (температура, помол, посуда)
    {"key": "grind",  "label": {"ru": "Помол"}, "text": {"ru": "Мелкий"}}
  ],
  "steps": [
    {
      "n": 1,
      "title": {"ru": "Смолоть кофе"},
      "text":  {"ru": "Смолите {coffee} кофе..."},   // {ключ} подставляется автоматически
      "tip":   {"ru": "Мелите перед приготовлением"},
      "timer": 27,               // секунды → таймер в пошаговом режиме
      "repeatable": true,        // для чая: кнопка «Следующий пролив»
      "timer_step": 5,           // шаг увеличения таймера
      "weight_check": {"ru": "{coffee}"}   // напоминание «проверьте вес»
    }
  ],
  "tips": [{"ru": "..."}]
}
```

Плейсхолдер `{ключ}` в тексте шага подставляется **уже пересчитанным** значением
с учётом числа порций и выбранной системы единиц.

## 6. Заметки по расширению

- Добавить рецепт — просто дописать объект в `app/data/recipes.json`.
- Схема БД — в `app/db.py` (`SCHEMA`); миграции удобно вешать на таблицу `meta`.
- Иконки напитков сейчас эмодзи (`icon`), при желании замените на PNG и
  отрисуйте через `kivy.uix.image.Image` в карточке.
