# -*- coding: utf-8 -*-
"""Отдельный экран с несколькими независимыми таймерами."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

from app.i18n import t
from app.screens.base import BaseScreen
from app.utils import play_beep, vibrate
from app.widgets import Btn, Card, Column, CountdownTimer, Input, TLabel, TopBar

PRESETS = [15, 30, 45, 60, 120, 180, 240, 300]


class TimersScreen(BaseScreen):
    def __init__(self, **kw):
        super(TimersScreen, self).__init__(**kw)
        self.timers = []
        self.root_box.add_widget(TopBar(t("timers"), on_back=self.app.pop))
        self.col = Column()
        self.root_box.add_widget(self.col)

        panel = Card(color_key="surface", padding=dp(12))
        row = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        self.min_in = Input(hint=t("min"), height=dp(46))
        self.sec_in = Input(hint=t("sec"), height=dp(46))
        self.min_in.text = "0"
        self.sec_in.text = "30"
        row.add_widget(self.min_in)
        row.add_widget(self.sec_in)
        row.add_widget(Btn(text=t("add_timer"), height=dp(46), size=13,
                           on_press_cb=self._add_custom))
        panel.add_widget(row)
        presets = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(6))
        for p in PRESETS[:5]:
            presets.add_widget(Btn(text="%ds" % p, bg="surface_alt", fg="text",
                                   height=dp(40), size=12,
                                   on_press_cb=lambda s=p: self._add(s)))
        panel.add_widget(presets)
        wrap = BoxLayout(size_hint_y=None, height=dp(120),
                         padding=[dp(16), dp(8), dp(16), dp(8)])
        wrap.add_widget(panel)
        self.root_box.add_widget(wrap)

    def _add_custom(self):
        try:
            total = int(self.min_in.text or 0) * 60 + int(self.sec_in.text or 0)
        except ValueError:
            total = 0
        if total > 0:
            self._add(total)

    def _add(self, seconds):
        timer = CountdownTimer(seconds, on_finish=self._finish,
                               label="%s %d" % (t("timers"), len(self.timers) + 1))
        self.timers.append(timer)
        self.col.add(timer)
        timer.start()

    def _finish(self):
        play_beep(self.app.user_dir)
        vibrate(0.6)

    def on_leave_screen(self):
        for tm in self.timers:
            tm.stop_clock()
