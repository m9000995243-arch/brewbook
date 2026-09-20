# -*- coding: utf-8 -*-
"""Звук, вибрация, «поделиться», всплывающие подсказки."""

import math
import os
import struct
import wave

from kivy.core.audio import SoundLoader
from kivy.clock import Clock

_sound = None


def ensure_beep(directory):
    """Сгенерировать wav-сигнал без внешних зависимостей."""
    path = os.path.join(directory, "beep.wav")
    if os.path.exists(path):
        return path
    rate, dur, freq = 44100, 0.18, 880.0
    frames = []
    for i in range(int(rate * dur)):
        env = min(1.0, i / 400.0, (int(rate * dur) - i) / 400.0)
        frames.append(struct.pack("<h", int(22000 * env * math.sin(2 * math.pi * freq * i / rate))))
    silence = struct.pack("<h", 0) * int(rate * 0.09)
    body = b"".join(frames)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(body + silence + body)
    return path


def play_beep(directory):
    global _sound
    try:
        if _sound is None:
            _sound = SoundLoader.load(ensure_beep(directory))
        if _sound:
            _sound.play()
    except Exception:
        pass


def vibrate(seconds=0.5):
    try:
        from plyer import vibrator
        vibrator.vibrate(seconds)
    except Exception:
        pass


def share_text(text, title="Recipe"):
    """Android: системный Intent. Десктоп: буфер обмена."""
    try:
        from jnius import autoclass, cast
        from android import mActivity  # noqa
        Intent = autoclass("android.content.Intent")
        String = autoclass("java.lang.String")
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.setType("text/plain")
        intent.putExtra(Intent.EXTRA_SUBJECT, cast("java.lang.CharSequence", String(title)))
        intent.putExtra(Intent.EXTRA_TEXT, cast("java.lang.CharSequence", String(text)))
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        chooser = Intent.createChooser(intent, cast("java.lang.CharSequence", String(title)))
        PythonActivity.mActivity.startActivity(chooser)
        return "android"
    except Exception:
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            return "clipboard"
        except Exception:
            return "none"


def toast(message, duration=1.6):
    """Простой тост поверх окна (работает и на десктопе, и на Android)."""
    from kivy.uix.label import Label
    from kivy.core.window import Window
    from kivy.metrics import sp, dp
    from kivy.graphics import Color, RoundedRectangle
    from app.theme import C

    lbl = Label(text=message, font_size=sp(14), color=C("text"),
                size_hint=(None, None), padding=(dp(16), dp(10)))
    lbl.texture_update()
    lbl.size = (min(Window.width - dp(40), lbl.texture_size[0] + dp(32)),
                lbl.texture_size[1] + dp(20))
    lbl.center_x = Window.width / 2
    lbl.y = dp(60)
    with lbl.canvas.before:
        Color(*C("surface_alt"))
        rect = RoundedRectangle(pos=lbl.pos, size=lbl.size, radius=[dp(12)])
    lbl.bind(pos=lambda *_: setattr(rect, "pos", lbl.pos),
             size=lambda *_: setattr(rect, "size", lbl.size))
    Window.add_widget(lbl)
    Clock.schedule_once(lambda *_: Window.remove_widget(lbl), duration)
