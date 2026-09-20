# -*- coding: utf-8 -*-
"""Модель рецепта + пересчёт по количеству порций."""

import re
import uuid

from app.i18n import tr, t
from app.units import convert_amount

_PLACEHOLDER = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def render(text, mapping):
    """Подставить {ключ_параметра} в текст шага. Неизвестные ключи не трогаем."""
    return _PLACEHOLDER.sub(lambda m: str(mapping.get(m.group(1), m.group(0))), text or "")


class Param(object):
    def __init__(self, data):
        self.key = data.get("key", "")
        self.label = data.get("label", {})
        self.value = data.get("value")
        self.unit = data.get("unit", "")
        self.text = data.get("text")
        self.scale = bool(data.get("scale", False))

    @property
    def title(self):
        return tr(self.label, self.key)

    def display(self, factor=1.0):
        if self.value is None:
            return tr(self.text, "—")
        return convert_amount(self.value, self.unit, factor if self.scale else 1.0)


class Step(object):
    def __init__(self, data, mapping, factor=1.0):
        self.n = data.get("n", 0)
        self.title = render(tr(data.get("title")), mapping)
        self.text = render(tr(data.get("text")), mapping)
        self.tip = render(tr(data.get("tip")), mapping)
        self.timer = data.get("timer")
        self.repeatable = bool(data.get("repeatable"))
        self.timer_step = data.get("timer_step", 5)
        self.weight_check = data.get("weight_check")
        if self.weight_check:
            self.weight_check = render(tr(self.weight_check), mapping)


class Recipe(object):
    def __init__(self, data):
        self.data = data
        self.id = data.get("id") or ("user_%s" % uuid.uuid4().hex[:8])
        self.kind = data.get("kind", "coffee")            # coffee | tea
        self.category = data.get("category", "base")      # base | author
        self.is_user = bool(data.get("is_user"))
        self.photo = data.get("photo")
        self.icon = data.get("icon", "☕" if self.kind == "coffee" else "🍵")
        self.base_servings = data.get("base_servings", 1)
        self.servings_options = data.get(
            "servings_options", [1, 2] if self.kind == "coffee" else [1, 2, 3])
        self._params = [Param(p) for p in data.get("params", [])]
        self._steps = data.get("steps", [])
        self.tips = data.get("tips", [])
        self.infusions = data.get("infusions") or {}

    # ---- локализованные поля -------------------------------------------
    @property
    def name(self):
        return tr(self.data.get("name"), "—")

    @property
    def desc(self):
        return tr(self.data.get("desc"), "")

    @property
    def subtitle(self):
        return tr(self.data.get("subtitle"), "")

    # ---- пересчёт -------------------------------------------------------
    def factor(self, servings):
        return float(servings) / float(self.base_servings or 1)

    def params(self, servings=1):
        return self._params

    def params_map(self, servings=1):
        f = self.factor(servings)
        return {p.key: p.display(f) for p in self._params}

    def steps(self, servings=1):
        f = self.factor(servings)
        mapping = self.params_map(servings)
        return [Step(s, mapping, f) for s in self._steps]

    def tips_list(self):
        return [tr(x) for x in self.tips]

    # ---- экспорт --------------------------------------------------------
    def as_text(self, servings=1):
        lines = [self.name, self.desc, ""]
        lines.append(t("params").upper())
        f = self.factor(servings)
        for p in self._params:
            lines.append(" • %s: %s" % (p.title, p.display(f)))
        lines.append("")
        lines.append(t("steps").upper())
        for s in self.steps(servings):
            lines.append("%d. %s" % (s.n, s.title))
            lines.append("   %s" % s.text)
            if s.tip:
                lines.append("   %s: %s" % (t("tip"), s.tip))
        tips = self.tips_list()
        if tips:
            lines.append("")
            lines.append(t("tips").upper())
            for x in tips:
                lines.append(" • %s" % x)
        return "\n".join(lines)

    def to_dict(self):
        return self.data
