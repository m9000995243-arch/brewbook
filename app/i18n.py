# -*- coding: utf-8 -*-
"""Локализация интерфейса: русский / английский."""

STRINGS = {
    "ru": {
        "app_title": "Кофе и Чай",
        "subtitle": "Справочник рецептов заваривания",
        "coffee": "Кофе", "tea": "Чай",
        "base": "Базовые", "author": "Интересные / Авторские",
        "favorites": "Избранное", "timers": "Таймеры",
        "settings": "Настройки", "editor": "Мои рецепты",
        "back": "< Назад", "params": "Параметры", "steps": "Пошаговый рецепт",
        "tips": "Лайфхаки и тонкости",
        "servings": "Количество порций", "people": "Количество человек",
        "cup_1": "1 чашка", "cup_2": "2 чашки",
        "p1": "1 чел.", "p2": "2 чел.", "p3": "3+ чел.",
        "start_step_mode": "Начать пошаговый режим",
        "fav_add": "Сохранить в избранное", "fav_remove": "Убрать из избранного",
        "share": "Поделиться рецептом", "notes": "Заметки",
        "notes_hint": "Ваши заметки по рецепту...", "save": "Сохранить",
        "saved": "Сохранено", "copied": "Скопировано в буфер обмена",
        "next": "Далее", "prev": "Назад", "start": "Старт", "pause": "Пауза",
        "reset": "Сброс", "done": "Готово!", "step": "Шаг",
        "next_infusion": "Следующий пролив (+{n} с)",
        "tip": "Лайфхак", "scale_note": "Проверьте вес на весах",
        "new_recipe": "Новый рецепт", "name": "Название",
        "short_desc": "Краткое описание", "kind": "Тип", "category": "Категория",
        "add_param": "+ параметр", "add_step": "+ шаг", "photo": "Фото напитка",
        "pick_photo": "Выбрать фото", "delete": "Удалить", "edit": "Редактировать",
        "label": "Название", "value": "Значение", "unit": "Ед.",
        "step_title": "Название шага", "step_text": "Описание",
        "step_tip": "Лайфхак", "step_timer": "Таймер, с",
        "sort_date": "По дате", "sort_alpha": "По алфавиту",
        "empty_fav": "Пока пусто. Откройте рецепт и нажмите «Сохранить в избранное».",
        "empty_user": "Своих рецептов ещё нет.",
        "add_timer": "+ Добавить таймер", "theme": "Тема",
        "dark": "Тёмная", "light": "Светлая", "units": "Единицы измерения",
        "metric": "Граммы / мл", "imperial": "Унции / fl oz",
        "language": "Язык интерфейса", "min": "мин", "sec": "с",
        "my_recipes": "Мои рецепты", "confirm_delete": "Удалить рецепт?",
        "yes": "Да", "no": "Нет", "ok": "ОК",
    },
    "en": {
        "app_title": "Coffee & Tea",
        "subtitle": "Brewing recipes handbook",
        "coffee": "Coffee", "tea": "Tea",
        "base": "Classic", "author": "Signature",
        "favorites": "Favorites", "timers": "Timers",
        "settings": "Settings", "editor": "My recipes",
        "back": "< Back", "params": "Parameters", "steps": "Step by step",
        "tips": "Tips & tricks",
        "servings": "Servings", "people": "People",
        "cup_1": "1 cup", "cup_2": "2 cups",
        "p1": "1 person", "p2": "2 people", "p3": "3+ people",
        "start_step_mode": "Start guided mode",
        "fav_add": "Add to favorites", "fav_remove": "Remove from favorites",
        "share": "Share recipe", "notes": "Notes",
        "notes_hint": "Your notes for this recipe...", "save": "Save",
        "saved": "Saved", "copied": "Copied to clipboard",
        "next": "Next", "prev": "Back", "start": "Start", "pause": "Pause",
        "reset": "Reset", "done": "Done!", "step": "Step",
        "next_infusion": "Next infusion (+{n}s)",
        "tip": "Tip", "scale_note": "Check the scale",
        "new_recipe": "New recipe", "name": "Name",
        "short_desc": "Short description", "kind": "Kind", "category": "Category",
        "add_param": "+ parameter", "add_step": "+ step", "photo": "Photo",
        "pick_photo": "Pick photo", "delete": "Delete", "edit": "Edit",
        "label": "Label", "value": "Value", "unit": "Unit",
        "step_title": "Step title", "step_text": "Description",
        "step_tip": "Tip", "step_timer": "Timer, s",
        "sort_date": "By date", "sort_alpha": "A-Z",
        "empty_fav": "Empty. Open a recipe and tap 'Add to favorites'.",
        "empty_user": "No custom recipes yet.",
        "add_timer": "+ Add timer", "theme": "Theme",
        "dark": "Dark", "light": "Light", "units": "Units",
        "metric": "Grams / ml", "imperial": "Ounces / fl oz",
        "language": "Language", "min": "min", "sec": "s",
        "my_recipes": "My recipes", "confirm_delete": "Delete recipe?",
        "yes": "Yes", "no": "No", "ok": "OK",
    },
}


class I18N:
    lang = "ru"

    @classmethod
    def set(cls, lang):
        cls.lang = lang if lang in STRINGS else "ru"


def t(key, **kw):
    s = STRINGS.get(I18N.lang, STRINGS["ru"]).get(key) or STRINGS["ru"].get(key, key)
    return s.format(**kw) if kw else s


def tr(value, default=""):
    """Достать локализованную строку из словаря {'ru': ..., 'en': ...}."""
    if value is None:
        return default
    if isinstance(value, str):
        return value
    return value.get(I18N.lang) or value.get("ru") or value.get("en") or default
