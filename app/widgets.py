# -*- coding: utf-8 -*-
"""Переиспользуемые виджеты: карточки, кнопки, сегментированный переключатель, таймер."""

from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from app.i18n import t
from app.theme import C
from app.units import fmt_seconds


# ---------------------------------------------------------------- базовые
class RoundedBox(BoxLayout):
    """BoxLayout со скруглённым фоном."""

    def __init__(self, color_key="surface", radius=14, auto_height=True, **kw):
        kw.setdefault("orientation", "vertical")
        kw.setdefault("padding", dp(14))
        kw.setdefault("spacing", dp(6))
        if auto_height:
            kw.setdefault("size_hint_y", None)
        super(RoundedBox, self).__init__(**kw)
        self.color_key = color_key
        with self.canvas.before:
            self._color = Color(*C(color_key))
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(radius)])
        self.bind(pos=self._sync, size=self._sync)
        if auto_height:
            self.bind(minimum_height=self.setter("height"))

    def _sync(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_color(self, color_key):
        self.color_key = color_key
        self._color.rgba = C(color_key)


class Card(RoundedBox):
    pass


class TapCard(ButtonBehavior, RoundedBox):
    pass


class TLabel(Label):
    """Label с автопереносом и авто-высотой."""

    def __init__(self, text="", size=15, bold=False, color_key="text",
                 halign="left", **kw):
        super(TLabel, self).__init__(
            text=text, font_size=sp(size), bold=bold, color=C(color_key),
            halign=halign, valign="top", size_hint_y=None, markup=True, **kw)
        self.bind(width=self._upd_ts, texture_size=self._upd_h)
        Clock.schedule_once(self._upd_ts, 0)

    def _upd_ts(self, *a):
        self.text_size = (self.width, None)

    def _upd_h(self, *a):
        self.height = self.texture_size[1]


class Btn(ButtonBehavior, BoxLayout):
    """Скруглённая кнопка с центрированным текстом."""

    def __init__(self, text="", on_press_cb=None, bg="primary", fg="on_primary",
                 height=dp(48), size=15, bold=True, **kw):
        kw.setdefault("size_hint_y", None)
        super(Btn, self).__init__(height=height, **kw)
        self.bg_key, self.fg_key = bg, fg
        with self.canvas.before:
            self._color = Color(*C(bg))
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._sync, size=self._sync)
        self.label = Label(text=text, font_size=sp(size), bold=bold, color=C(fg),
                           halign="center", valign="middle", markup=True)
        self.label.bind(size=lambda *_: setattr(self.label, "text_size", self.label.size))
        self.add_widget(self.label)
        if on_press_cb:
            self.bind(on_release=lambda *_: on_press_cb())

    def _sync(self, *a):
        self._rect.pos = self.pos
        self._rect.size = self.size

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, value):
        self.label.text = value

    def set_style(self, bg, fg):
        self.bg_key, self.fg_key = bg, fg
        self._color.rgba = C(bg)
        self.label.color = C(fg)


class Segmented(BoxLayout):
    """Переключатель из нескольких кнопок (порции / вкладки / сортировка)."""

    def __init__(self, options, on_change=None, index=0, **kw):
        kw.setdefault("size_hint_y", None)
        kw.setdefault("height", dp(44))
        kw.setdefault("spacing", dp(8))
        super(Segmented, self).__init__(**kw)
        self.on_change = on_change
        self.index = index
        self.buttons = []
        for i, (label, value) in enumerate(options):
            b = Btn(text=label, height=dp(44), size=14,
                    on_press_cb=(lambda idx=i: self.select(idx)))
            b.value = value
            self.buttons.append(b)
            self.add_widget(b)
        self._restyle()

    def _restyle(self):
        for i, b in enumerate(self.buttons):
            if i == self.index:
                b.set_style("primary", "on_primary")
            else:
                b.set_style("surface_alt", "text_muted")

    def select(self, idx, notify=True):
        self.index = idx
        self._restyle()
        if notify and self.on_change:
            self.on_change(self.buttons[idx].value)

    @property
    def value(self):
        return self.buttons[self.index].value


class Column(ScrollView):
    """Вертикальный скролл-контейнер."""

    def __init__(self, padding=dp(16), spacing=dp(12), **kw):
        super(Column, self).__init__(**kw)
        self.box = BoxLayout(orientation="vertical", size_hint_y=None,
                             padding=padding, spacing=spacing)
        self.box.bind(minimum_height=self.box.setter("height"))
        self.add_widget(self.box)

    def add(self, widget):
        self.box.add_widget(widget)
        return widget

    def clear(self):
        self.box.clear_widgets()


class Input(TextInput):
    def __init__(self, hint="", multiline=False, height=dp(46), **kw):
        super(Input, self).__init__(
            hint_text=hint, multiline=multiline, size_hint_y=None, height=height,
            background_color=C("surface_alt"), foreground_color=C("text"),
            cursor_color=C("primary"), hint_text_color=C("text_muted"),
            padding=[dp(10), dp(12), dp(10), dp(12)], font_size=sp(15), **kw)


class TopBar(BoxLayout):
    def __init__(self, title, on_back=None, right=None, **kw):
        kw.setdefault("size_hint_y", None)
        kw.setdefault("height", dp(56))
        kw.setdefault("padding", [dp(10), dp(6), dp(10), dp(6)])
        kw.setdefault("spacing", dp(8))
        super(TopBar, self).__init__(**kw)
        if on_back:
            back = Btn(text=t("back"), bg="surface_alt", fg="text", height=dp(40),
                       size=13, size_hint_x=None, width=dp(104),
                       on_press_cb=on_back)
            self.add_widget(back)
        lbl = Label(text=title, font_size=sp(18), bold=True, color=C("text"),
                    halign="left", valign="middle", shorten=True)
        lbl.bind(size=lambda *_: setattr(lbl, "text_size", lbl.size))
        self.add_widget(lbl)
        if right:
            self.add_widget(right)


class Row(BoxLayout):
    """Строка «подпись — значение»."""

    def __init__(self, left, right, **kw):
        kw.setdefault("size_hint_y", None)
        kw.setdefault("spacing", dp(8))
        super(Row, self).__init__(orientation="horizontal", **kw)
        a = TLabel(text=left, size=14, color_key="text_muted")
        b = TLabel(text=right, size=14, bold=True, halign="right")
        a.size_hint_x = 0.55
        b.size_hint_x = 0.45
        self.add_widget(a)
        self.add_widget(b)
        a.bind(height=self._sync)
        b.bind(height=self._sync)

    def _sync(self, *a):
        self.height = max(c.height for c in self.children)


class CountdownTimer(Card):
    """Таймер обратного отсчёта с кнопками Старт/Пауза/Сброс."""

    def __init__(self, seconds, on_finish=None, label="", **kw):
        super(CountdownTimer, self).__init__(color_key="surface_alt", **kw)
        self.total = int(seconds)
        self.left = float(seconds)
        self.running = False
        self.on_finish = on_finish
        self._event = None

        if label:
            self.add_widget(TLabel(text=label, size=13, color_key="text_muted"))
        self.display = TLabel(text=fmt_seconds(self.left), size=34, bold=True,
                              halign="center", color_key="primary")
        self.add_widget(self.display)
        row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        self.btn_start = Btn(text=t("start"), height=dp(44), size=14,
                             on_press_cb=self.toggle)
        row.add_widget(self.btn_start)
        row.add_widget(Btn(text=t("reset"), bg="surface", fg="text", height=dp(44),
                           size=14, on_press_cb=self.reset))
        self.add_widget(row)

    def set_total(self, seconds):
        self.total = int(seconds)
        self.reset()

    def toggle(self):
        if self.running:
            self.pause()
        else:
            self.start()

    def start(self):
        if self.left <= 0:
            self.left = float(self.total)
        self.running = True
        self.btn_start.text = t("pause")
        if self._event:
            self._event.cancel()
        self._event = Clock.schedule_interval(self._tick, 0.1)

    def pause(self):
        self.running = False
        self.btn_start.text = t("start")
        if self._event:
            self._event.cancel()
            self._event = None

    def reset(self):
        self.pause()
        self.left = float(self.total)
        self.display.text = fmt_seconds(self.left)
        self.display.color = C("primary")

    def _tick(self, dt):
        self.left -= dt
        if self.left <= 0:
            self.left = 0
            self.display.text = t("done")
            self.display.color = C("accent")
            self.pause()
            if self.on_finish:
                self.on_finish()
            return False
        self.display.text = fmt_seconds(self.left)

    def stop_clock(self):
        if self._event:
            self._event.cancel()
            self._event = None
