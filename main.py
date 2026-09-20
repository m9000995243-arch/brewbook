# -*- coding: utf-8 -*-
"""
Кофе и Чай — офлайн-справочник рецептов заваривания.
Python + Kivy. Точка входа приложения.
"""

import os
import sys

from kivy.config import Config

# На десктопе — вертикальный «телефонный» формат для отладки.
if sys.platform not in ("android",):
    Config.set("graphics", "width", "420")
    Config.set("graphics", "height", "860")

from kivy.app import App                      # noqa: E402
from kivy.core.window import Window           # noqa: E402
from kivy.uix.screenmanager import ScreenManager, SlideTransition, NoTransition  # noqa: E402

from app.db import Storage                    # noqa: E402
from app.i18n import I18N                     # noqa: E402
from app.theme import Theme                   # noqa: E402
from app.units import Units                   # noqa: E402
from app.screens.editor import EditorScreen               # noqa: E402
from app.screens.favorites import FavoritesScreen, MyRecipesScreen  # noqa: E402
from app.screens.home import HomeScreen                   # noqa: E402
from app.screens.recipe_detail import RecipeDetailScreen  # noqa: E402
from app.screens.recipe_list import RecipeListScreen      # noqa: E402
from app.screens.settings import SettingsScreen           # noqa: E402
from app.screens.step_mode import StepModeScreen          # noqa: E402
from app.screens.timers import TimersScreen               # noqa: E402

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_JSON = os.path.join(BASE_DIR, "app", "data", "recipes.json")

SCREENS = {
    "home": HomeScreen,
    "list": RecipeListScreen,
    "detail": RecipeDetailScreen,
    "step_mode": StepModeScreen,
    "favorites": FavoritesScreen,
    "my_recipes": MyRecipesScreen,
    "editor": EditorScreen,
    "timers": TimersScreen,
    "settings": SettingsScreen,
}


class BrewBookApp(App):
    title = "Кофе и Чай"

    def build(self):
        self.user_dir = self.user_data_dir
        os.makedirs(self.user_dir, exist_ok=True)

        self.store = Storage(os.path.join(self.user_dir, "brewbook.db"), SEED_JSON)
        self.settings_data = self.store.get_settings()
        self._apply_settings()

        self.sm = ScreenManager(transition=SlideTransition(duration=0.18))
        self._counter = 0
        self.stack = []
        self.push("home", root=True)

        Window.bind(on_keyboard=self._on_keyboard)
        return self.sm

    # ---- настройки ------------------------------------------------------
    @property
    def settings(self):
        return self.settings_data

    def _apply_settings(self):
        Theme.set(self.settings_data.get("theme", "dark"))
        Units.set(self.settings_data.get("units", "metric"))
        I18N.set(self.settings_data.get("lang", "ru"))

    def change_setting(self, key, value):
        self.settings_data[key] = value
        self.store.set_setting(key, value)
        self._apply_settings()
        self.rebuild()

    def rebuild(self):
        """Пересобрать интерфейс после смены темы/языка/единиц."""
        stack = list(self.stack)
        self.sm.transition = NoTransition()
        for name, _kw, screen in stack:
            screen.on_leave_screen()
            self.sm.remove_widget(screen)
        self.stack = []
        for name, kw, _screen in stack:
            self.push(name, root=(name == "home"), **kw)
        self.sm.transition = SlideTransition(duration=0.18)

    # ---- навигация ------------------------------------------------------
    def push(self, name, root=False, **kwargs):
        self._counter += 1
        screen = SCREENS[name](name="%s-%d" % (name, self._counter), **kwargs)
        self.sm.add_widget(screen)
        self.stack.append((name, kwargs, screen))
        self.sm.transition.direction = "left"
        self.sm.current = screen.name
        return screen

    def pop(self):
        if len(self.stack) <= 1:
            return
        name, kwargs, screen = self.stack.pop()
        prev = self.stack[-1][2]
        self.sm.transition.direction = "right"
        self.sm.current = prev.name
        screen.on_leave_screen()
        from kivy.clock import Clock
        Clock.schedule_once(lambda *_: self.sm.remove_widget(screen), 0.25)

    def _on_keyboard(self, window, key, *args):
        # 27 — Back на Android / Esc на десктопе
        if key == 27:
            if len(self.stack) > 1:
                self.pop()
                return True
        return False

    def on_pause(self):
        return True


if __name__ == "__main__":
    BrewBookApp().run()
