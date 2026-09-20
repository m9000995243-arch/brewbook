# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from app.theme import C


class BaseScreen(Screen):
    """Экран с фоном темы и вертикальной раскладкой (self.root_box)."""

    def __init__(self, **kw):
        super(BaseScreen, self).__init__(**kw)
        with self.canvas.before:
            Color(*C("bg"))
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync_bg, size=self._sync_bg)
        self.root_box = BoxLayout(orientation="vertical")
        self.add_widget(self.root_box)

    def _sync_bg(self, *a):
        self._bg.pos = self.pos
        self._bg.size = self.size

    @property
    def app(self):
        return App.get_running_app()

    def on_leave_screen(self):
        """Вызывается приложением перед удалением экрана (остановить таймеры и т.п.)."""
        pass
