# -*- coding: utf-8 -*-
"""Пересчёт граммовок/объёмов и форматирование значений."""

from app.i18n import I18N

G_TO_OZ = 1.0 / 28.3495
ML_TO_FLOZ = 1.0 / 29.5735


class Units:
    system = "metric"          # metric | imperial

    @classmethod
    def set(cls, system):
        cls.system = system if system in ("metric", "imperial") else "metric"


def _fmt_num(x):
    if x >= 100:
        return str(int(round(x)))
    if abs(x - round(x)) < 0.05:
        return str(int(round(x)))
    return ("%.1f" % x)


def _convert(value, unit):
    """Вернуть (число, подпись единицы) с учётом системы измерения."""
    if unit == "g":
        if Units.system == "imperial":
            return value * G_TO_OZ, "oz"
        return value, ("г" if I18N.lang == "ru" else "g")
    if unit == "ml":
        if Units.system == "imperial":
            return value * ML_TO_FLOZ, "fl oz"
        return value, ("мл" if I18N.lang == "ru" else "ml")
    if unit == "s":
        return value, ("с" if I18N.lang == "ru" else "s")
    if unit == "c":
        return value, "°C"
    if unit == "bar":
        return value, ("бар" if I18N.lang == "ru" else "bar")
    return value, unit


def convert_amount(value, unit="", factor=1.0):
    """value: число или [min, max]. Возвращает готовую строку."""
    if value is None:
        return "—"
    if isinstance(value, (list, tuple)):
        lo, _u = _convert(value[0] * factor, unit)
        hi, u = _convert(value[1] * factor, unit)
        body = "%s–%s" % (_fmt_num(lo), _fmt_num(hi))
    else:
        num, u = _convert(value * factor, unit)
        body = _fmt_num(num)
    return (body + " " + u).strip()


def fmt_seconds(total):
    total = int(max(0, total))
    return "%02d:%02d" % (total // 60, total % 60)
