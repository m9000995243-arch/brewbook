# -*- coding: utf-8 -*-
"""Настройки: тема, единицы измерения, язык интерфейса."""

from app.i18n import t
from app.screens.base import BaseScreen
from app.widgets import Card, Column, Segmented, TLabel, TopBar


class SettingsScreen(BaseScreen):
    def __init__(self, **kw):
        super(SettingsScreen, self).__init__(**kw)
        self.root_box.add_widget(TopBar(t("settings"), on_back=self.app.pop))
        col = Column()
        self.root_box.add_widget(col)
        s = self.app.settings

        col.add(self._block(t("theme"),
                            [(t("dark"), "dark"), (t("light"), "light")],
                            s.get("theme", "dark"), "theme"))
        col.add(self._block(t("units"),
                            [(t("metric"), "metric"), (t("imperial"), "imperial")],
                            s.get("units", "metric"), "units"))
        col.add(self._block(t("language"),
                            [("Русский", "ru"), ("English", "en")],
                            s.get("lang", "ru"), "lang"))

    def _block(self, title, options, current, key):
        card = Card(color_key="surface")
        card.add_widget(TLabel(text=title, size=15, bold=True, color_key="primary"))
        values = [o[1] for o in options]
        idx = values.index(current) if current in values else 0
        card.add_widget(Segmented(options, index=idx,
                                  on_change=lambda v, k=key: self.app.change_setting(k, v)))
        return card
