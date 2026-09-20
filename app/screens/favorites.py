# -*- coding: utf-8 -*-
"""Избранное и список пользовательских рецептов."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from app.i18n import t
from app.screens.base import BaseScreen
from app.widgets import Btn, Column, Segmented, TLabel, TapCard, TopBar


class FavoritesScreen(BaseScreen):
    def __init__(self, **kw):
        super(FavoritesScreen, self).__init__(**kw)
        self.sort = "date"
        self.root_box.add_widget(TopBar(t("favorites"), on_back=self.app.pop))

        wrap = BoxLayout(size_hint_y=None, height=dp(56),
                         padding=[dp(16), 0, dp(16), dp(8)])
        wrap.add_widget(Segmented([(t("sort_date"), "date"), (t("sort_alpha"), "alpha")],
                                  on_change=self._on_sort))
        self.root_box.add_widget(wrap)

        self.col = Column()
        self.root_box.add_widget(self.col)
        self._render()

    def _on_sort(self, value):
        self.sort = value
        self._render()

    def _render(self):
        self.col.clear()
        items = self.app.store.favorites(self.sort)
        if not items:
            self.col.add(TLabel(text=t("empty_fav"), size=14, color_key="text_muted"))
            return
        for r in items:
            card = TapCard(color_key="surface")
            head = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))
            head.add_widget(TLabel(text=r.icon, size=20, size_hint_x=None, width=dp(30)))
            head.add_widget(TLabel(text=r.name, size=17, bold=True))
            card.add_widget(head)
            card.add_widget(TLabel(text=r.desc, size=12, color_key="text_muted"))
            card.bind(on_release=lambda *_, rid=r.id: self.app.push("detail", recipe_id=rid))
            self.col.add(card)


class MyRecipesScreen(BaseScreen):
    def __init__(self, **kw):
        super(MyRecipesScreen, self).__init__(**kw)
        self.root_box.add_widget(TopBar(t("my_recipes"), on_back=self.app.pop))
        self.col = Column()
        self.root_box.add_widget(self.col)

        bar = BoxLayout(size_hint_y=None, height=dp(62), spacing=dp(10),
                        padding=[dp(16), 0, dp(16), dp(12)])
        bar.add_widget(Btn(text="+  " + t("new_recipe"),
                           on_press_cb=lambda: self.app.push("editor")))
        self.root_box.add_widget(bar)
        self._render()

    def _render(self):
        self.col.clear()
        items = self.app.store.user_recipes()
        if not items:
            self.col.add(TLabel(text=t("empty_user"), size=14, color_key="text_muted"))
            return
        for r in items:
            card = TapCard(color_key="surface")
            card.add_widget(TLabel(text="%s %s" % (r.icon, r.name), size=17, bold=True))
            card.add_widget(TLabel(text=r.desc, size=12, color_key="text_muted"))
            row = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(8))
            row.add_widget(Btn(text=t("edit"), bg="surface_alt", fg="text", size=12,
                               height=dp(40),
                               on_press_cb=lambda rid=r.id: self.app.push("editor", recipe_id=rid)))
            row.add_widget(Btn(text=t("delete"), bg="danger", fg="text", size=12,
                               height=dp(40),
                               on_press_cb=lambda rid=r.id: self._delete(rid)))
            card.add_widget(row)
            card.bind(on_release=lambda *_, rid=r.id: self.app.push("detail", recipe_id=rid))
            self.col.add(card)

    def _delete(self, recipe_id):
        self.app.store.delete_user_recipe(recipe_id)
        self._render()
