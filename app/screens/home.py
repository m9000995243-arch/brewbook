# -*- coding: utf-8 -*-
"""Главный экран: выбор «Кофе» / «Чай» + быстрые разделы."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from app.i18n import t
from app.screens.base import BaseScreen
from app.widgets import Btn, Column, TLabel, TapCard


class HomeScreen(BaseScreen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        col = Column(padding=dp(20), spacing=dp(16))
        self.root_box.add_widget(col)

        col.add(TLabel(text=t("app_title"), size=30, bold=True))
        col.add(TLabel(text=t("subtitle"), size=14, color_key="text_muted"))

        col.add(self._big_card("☕", t("coffee"),
                               "Эспрессо, капучино, латте, раф, авторские рецепты"
                               if t("coffee") == "Кофе" else
                               "Espresso, cappuccino, latte, raf, signature drinks",
                               lambda: self.app.push("list", kind="coffee")))
        col.add(self._big_card("🍵", t("tea"),
                               "Пуэры, улуны, зелёный, белый, авторские проливы"
                               if t("tea") == "Чай" else
                               "Puer, oolong, green, white, signature brews",
                               lambda: self.app.push("list", kind="tea")))

        grid = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        grid.add_widget(Btn(text=t("favorites"), bg="surface_alt", fg="text", size=13,
                            on_press_cb=lambda: self.app.push("favorites")))
        grid.add_widget(Btn(text=t("timers"), bg="surface_alt", fg="text", size=13,
                            on_press_cb=lambda: self.app.push("timers")))
        col.add(grid)

        grid2 = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        grid2.add_widget(Btn(text=t("my_recipes"), bg="surface_alt", fg="text", size=13,
                             on_press_cb=lambda: self.app.push("my_recipes")))
        grid2.add_widget(Btn(text=t("settings"), bg="surface_alt", fg="text", size=13,
                             on_press_cb=lambda: self.app.push("settings")))
        col.add(grid2)

    def _big_card(self, icon, title, subtitle, cb):
        card = TapCard(color_key="surface", padding=dp(20), spacing=dp(6))
        card.add_widget(TLabel(text=icon, size=42, halign="left"))
        card.add_widget(TLabel(text=title, size=24, bold=True, color_key="primary"))
        card.add_widget(TLabel(text=subtitle, size=13, color_key="text_muted"))
        card.bind(on_release=lambda *_: cb())
        return card
