# -*- coding: utf-8 -*-
"""Экран детального рецепта: параметры, пошаговый список, лайфхаки, заметки."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from app.i18n import t
from app.screens.base import BaseScreen
from app.utils import share_text, toast
from app.widgets import Btn, Card, Column, Input, Row, Segmented, TLabel, TopBar


class RecipeDetailScreen(BaseScreen):
    def __init__(self, recipe_id=None, **kw):
        super(RecipeDetailScreen, self).__init__(**kw)
        self.recipe = self.app.store.get_recipe(recipe_id)
        self.servings = self.recipe.servings_options[0] if self.recipe else 1

        title = self.recipe.name if self.recipe else "—"
        self.root_box.add_widget(TopBar(title, on_back=self.app.pop))

        self.col = Column()
        self.root_box.add_widget(self.col)
        if self.recipe:
            self._render()

    # ------------------------------------------------------------------
    def _servings_options(self):
        r = self.recipe
        if r.kind == "coffee":
            labels = {1: t("cup_1"), 2: t("cup_2")}
        else:
            labels = {1: t("p1"), 2: t("p2"), 3: t("p3")}
        return [(labels.get(n, str(n)), n) for n in r.servings_options]

    def _on_servings(self, value):
        self.servings = value
        self._render()

    # ------------------------------------------------------------------
    def _render(self):
        r = self.recipe
        self.col.clear()
        add = self.col.add

        if r.photo:
            try:
                img = Image(source=r.photo, size_hint_y=None, height=dp(180),
                            allow_stretch=True, keep_ratio=True)
                add(img)
            except Exception:
                pass

        add(TLabel(text="%s %s" % (r.icon, r.name), size=26, bold=True))
        if r.subtitle:
            add(TLabel(text=r.subtitle, size=13, color_key="primary"))
        add(TLabel(text=r.desc, size=14, color_key="text_muted"))

        # --- переключатель порций
        add(TLabel(text=t("servings") if r.kind == "coffee" else t("people"),
                   size=13, color_key="text_muted"))
        opts = self._servings_options()
        idx = [o[1] for o in opts].index(self.servings) if self.servings in [o[1] for o in opts] else 0
        add(Segmented(opts, on_change=self._on_servings, index=idx))

        # --- параметры
        params_card = Card(color_key="surface")
        params_card.add_widget(TLabel(text=t("params"), size=16, bold=True,
                                      color_key="primary"))
        f = r.factor(self.servings)
        for p in r.params(self.servings):
            params_card.add_widget(Row(p.title, p.display(f)))
        add(params_card)

        # --- шаги
        add(TLabel(text=t("steps"), size=18, bold=True))
        for s in r.steps(self.servings):
            add(self._step_card(s))

        # --- лайфхаки
        tips = r.tips_list()
        if tips:
            tips_card = Card(color_key="surface")
            tips_card.add_widget(TLabel(text=t("tips"), size=16, bold=True,
                                        color_key="primary"))
            for x in tips:
                tips_card.add_widget(TLabel(text="•  " + x, size=13,
                                            color_key="text_muted"))
            add(tips_card)

        # --- пошаговый режим
        add(Btn(text="▶  " + t("start_step_mode"), height=dp(52),
                on_press_cb=lambda: self.app.push(
                    "step_mode", recipe_id=r.id, servings=self.servings)))

        # --- избранное / поделиться
        row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.fav_btn = Btn(text=self._fav_label(), bg="surface_alt", fg="text",
                           size=13, on_press_cb=self._toggle_fav)
        row.add_widget(self.fav_btn)
        row.add_widget(Btn(text=t("share"), bg="surface_alt", fg="text", size=13,
                           on_press_cb=self._share))
        add(row)

        # --- заметки
        notes_card = Card(color_key="surface")
        notes_card.add_widget(TLabel(text=t("notes"), size=16, bold=True,
                                     color_key="primary"))
        self.note_input = Input(hint=t("notes_hint"), multiline=True, height=dp(110))
        self.note_input.text = self.app.store.get_note(r.id)
        notes_card.add_widget(self.note_input)
        notes_card.add_widget(Btn(text=t("save"), height=dp(42), size=13,
                                  on_press_cb=self._save_note))
        add(notes_card)

    def _step_card(self, s):
        card = Card(color_key="surface")
        head = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))
        num = TLabel(text=str(s.n), size=18, bold=True, color_key="primary",
                     size_hint_x=None, width=dp(26))
        ttl = TLabel(text=s.title, size=16, bold=True)
        head.add_widget(num)
        head.add_widget(ttl)
        card.add_widget(head)
        card.add_widget(TLabel(text=s.text, size=14))
        if s.tip:
            card.add_widget(TLabel(text="💡 %s: %s" % (t("tip"), s.tip), size=12,
                                   color_key="accent"))
        if s.timer:
            card.add_widget(TLabel(text="⏱ %s %s" % (s.timer, t("sec")), size=12,
                                   color_key="text_muted"))
        return card

    # ------------------------------------------------------------------
    def _fav_label(self):
        return t("fav_remove") if self.app.store.is_favorite(self.recipe.id) else t("fav_add")

    def _toggle_fav(self):
        added = self.app.store.toggle_favorite(self.recipe.id)
        self.fav_btn.text = self._fav_label()
        toast(t("saved") if added else t("ok"))

    def _share(self):
        result = share_text(self.recipe.as_text(self.servings), self.recipe.name)
        if result == "clipboard":
            toast(t("copied"))

    def _save_note(self):
        self.app.store.set_note(self.recipe.id, self.note_input.text)
        toast(t("saved"))
