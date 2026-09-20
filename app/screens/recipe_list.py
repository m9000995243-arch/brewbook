# -*- coding: utf-8 -*-
"""Список рецептов выбранной категории с вкладками «Базовые» / «Авторские»."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from app.i18n import t
from app.screens.base import BaseScreen
from app.widgets import Column, Segmented, TLabel, TapCard, TopBar


class RecipeListScreen(BaseScreen):
    def __init__(self, kind="coffee", **kw):
        super(RecipeListScreen, self).__init__(**kw)
        self.kind = kind
        self.root_box.add_widget(TopBar(t(kind), on_back=self.app.pop))

        tabs = Segmented([(t("base"), "base"), (t("author"), "author")],
                         on_change=self._on_tab)
        wrap = BoxLayout(size_hint_y=None, height=dp(56), padding=[dp(16), 0, dp(16), dp(8)])
        wrap.add_widget(tabs)
        self.root_box.add_widget(wrap)

        self.col = Column()
        self.root_box.add_widget(self.col)
        self._render("base")

    def _on_tab(self, value):
        self._render(value)

    def _render(self, category):
        self.col.clear()
        recipes = self.app.store.recipes(kind=self.kind, category=category)
        if not recipes:
            self.col.add(TLabel(text=t("empty_user"), size=14, color_key="text_muted"))
            return
        for r in recipes:
            self.col.add(self._card(r))

    def _card(self, recipe):
        card = TapCard(color_key="surface", padding=dp(14), spacing=dp(4))
        head = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(10))
        icon = TLabel(text=recipe.icon, size=24, size_hint_x=None, width=dp(34))
        name = TLabel(text=recipe.name, size=18, bold=True)
        head.add_widget(icon)
        head.add_widget(name)
        card.add_widget(head)
        if recipe.subtitle:
            card.add_widget(TLabel(text=recipe.subtitle, size=12, color_key="primary"))
        card.add_widget(TLabel(text=recipe.desc, size=13, color_key="text_muted"))
        card.bind(on_release=lambda *_: self.app.push("detail", recipe_id=recipe.id))
        return card
