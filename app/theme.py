# -*- coding: utf-8 -*-
"""Цветовые палитры приложения (тёплые тёмные / карамельные тона)."""

PALETTES = {
    "dark": {
        "bg":          (0.086, 0.070, 0.062, 1),
        "surface":     (0.149, 0.121, 0.105, 1),
        "surface_alt": (0.204, 0.164, 0.137, 1),
        "primary":     (0.855, 0.600, 0.329, 1),
        "primary_dim": (0.482, 0.345, 0.196, 1),
        "on_primary":  (0.110, 0.086, 0.070, 1),
        "text":        (0.960, 0.925, 0.878, 1),
        "text_muted":  (0.690, 0.627, 0.568, 1),
        "accent":      (0.545, 0.702, 0.541, 1),
        "danger":      (0.839, 0.380, 0.341, 1),
        "line":        (0.270, 0.223, 0.192, 1),
    },
    "light": {
        "bg":          (0.980, 0.960, 0.933, 1),
        "surface":     (1.000, 0.992, 0.976, 1),
        "surface_alt": (0.949, 0.913, 0.862, 1),
        "primary":     (0.705, 0.443, 0.180, 1),
        "primary_dim": (0.878, 0.792, 0.686, 1),
        "on_primary":  (1.000, 0.992, 0.976, 1),
        "text":        (0.157, 0.125, 0.105, 1),
        "text_muted":  (0.427, 0.376, 0.333, 1),
        "accent":      (0.263, 0.482, 0.286, 1),
        "danger":      (0.729, 0.235, 0.200, 1),
        "line":        (0.874, 0.827, 0.760, 1),
    },
}


class Theme:
    name = "dark"

    @classmethod
    def set(cls, name):
        cls.name = name if name in PALETTES else "dark"

    @classmethod
    def c(cls, key):
        return PALETTES[cls.name].get(key, (1, 0, 1, 1))


def C(key):
    """Короткий доступ к цвету текущей темы."""
    return Theme.c(key)
