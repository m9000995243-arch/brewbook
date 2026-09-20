# -*- coding: utf-8 -*-
"""Режим «поварёнка»: по одному шагу за раз, с таймерами и напоминаниями о весах."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from app.i18n import t
from app.screens.base import BaseScreen
from app.utils import play_beep, vibrate
from app.widgets import Btn, Card, Column, CountdownTimer, TLabel, TopBar


class StepModeScreen(BaseScreen):
    def __init__(self, recipe_id=None, servings=1, **kw):
        super(StepModeScreen, self).__init__(**kw)
        self.recipe = self.app.store.get_recipe(recipe_id)
        self.servings = servings
        self.steps = self.recipe.steps(servings) if self.recipe else []
        self.index = 0
        self.timer = None
        self.extra = 0        # накопленная добавка к таймеру пролива

        self.root_box.add_widget(TopBar(self.recipe.name if self.recipe else "—",
                                        on_back=self.app.pop))
        self.col = Column()
        self.root_box.add_widget(self.col)

        nav = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10),
                        padding=[dp(16), 0, dp(16), dp(12)])
        self.btn_prev = Btn(text=t("prev"), bg="surface_alt", fg="text",
                            on_press_cb=self.prev)
        self.btn_next = Btn(text=t("next"), on_press_cb=self.next)
        nav.add_widget(self.btn_prev)
        nav.add_widget(self.btn_next)
        self.root_box.add_widget(nav)

        self._render()

    # ------------------------------------------------------------------
    def _render(self):
        self._stop_timer()
        self.col.clear()
        if not self.steps:
            return
        s = self.steps[self.index]

        self.col.add(TLabel(
            text="%s %d / %d" % (t("step"), self.index + 1, len(self.steps)),
            size=13, color_key="text_muted", halign="center"))
        self.col.add(TLabel(text=s.title, size=26, bold=True, halign="center",
                            color_key="primary"))

        card = Card(color_key="surface", padding=dp(18))
        card.add_widget(TLabel(text=s.text, size=17))
        if s.tip:
            card.add_widget(TLabel(text="💡 %s: %s" % (t("tip"), s.tip), size=13,
                                   color_key="accent"))
        self.col.add(card)

        if s.weight_check:
            warn = Card(color_key="surface_alt")
            warn.add_widget(TLabel(text="⚖  %s: %s" % (t("scale_note"), s.weight_check),
                                   size=14, bold=True))
            self.col.add(warn)

        if s.timer:
            self.timer = CountdownTimer(int(s.timer) + self.extra,
                                        on_finish=self._on_timer_done)
            self.col.add(self.timer)
            if s.repeatable:
                step = int(s.timer_step or 5)
                self.col.add(Btn(text=t("next_infusion", n=step), bg="surface_alt",
                                 fg="text", height=dp(46), size=14,
                                 on_press_cb=lambda st=step: self._next_infusion(st)))

        self.btn_prev.opacity = 0 if self.index == 0 else 1
        self.btn_next.text = t("done") if self.index == len(self.steps) - 1 else t("next")

    def _next_infusion(self, step):
        self.extra += step
        if self.timer:
            self.timer.set_total(int(self.steps[self.index].timer) + self.extra)
            self.timer.start()

    def _on_timer_done(self):
        play_beep(self.app.user_dir)
        vibrate(0.6)

    def _stop_timer(self):
        if self.timer:
            self.timer.stop_clock()
            self.timer = None

    # ------------------------------------------------------------------
    def next(self):
        if self.index >= len(self.steps) - 1:
            self.app.pop()
            return
        self.index += 1
        self.extra = 0
        self._render()

    def prev(self):
        if self.index == 0:
            return
        self.index -= 1
        self.extra = 0
        self._render()

    def on_leave_screen(self):
        self._stop_timer()
