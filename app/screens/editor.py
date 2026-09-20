# -*- coding: utf-8 -*-
"""Редактор пользовательских рецептов (кофе/чай) по тому же шаблону."""

import uuid

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

from app.i18n import t
from app.screens.base import BaseScreen
from app.utils import toast
from app.widgets import Btn, Card, Column, Input, Segmented, TLabel, TopBar


class EditorScreen(BaseScreen):
    def __init__(self, recipe_id=None, **kw):
        super(EditorScreen, self).__init__(**kw)
        self.recipe_id = recipe_id
        existing = self.app.store.get_recipe(recipe_id) if recipe_id else None
        self.data = dict(existing.data) if existing else {}
        self.photo_path = self.data.get("photo")
        self.param_rows = []
        self.step_rows = []

        self.root_box.add_widget(TopBar(t("new_recipe") if not existing else t("edit"),
                                        on_back=self.app.pop))
        self.col = Column()
        self.root_box.add_widget(self.col)

        # --- основные поля
        base = Card(color_key="surface")
        self.name_in = Input(hint=t("name"))
        self.name_in.text = self.data.get("name", {}).get("ru", "") if isinstance(
            self.data.get("name"), dict) else (self.data.get("name") or "")
        self.desc_in = Input(hint=t("short_desc"), multiline=True, height=dp(80))
        self.desc_in.text = self.data.get("desc", {}).get("ru", "") if isinstance(
            self.data.get("desc"), dict) else (self.data.get("desc") or "")
        base.add_widget(TLabel(text=t("name"), size=13, color_key="text_muted"))
        base.add_widget(self.name_in)
        base.add_widget(TLabel(text=t("short_desc"), size=13, color_key="text_muted"))
        base.add_widget(self.desc_in)

        base.add_widget(TLabel(text=t("kind"), size=13, color_key="text_muted"))
        kinds = [(t("coffee"), "coffee"), (t("tea"), "tea")]
        kidx = 1 if self.data.get("kind") == "tea" else 0
        self.kind_seg = Segmented(kinds, index=kidx)
        base.add_widget(self.kind_seg)

        base.add_widget(TLabel(text=t("category"), size=13, color_key="text_muted"))
        cats = [(t("base"), "base"), (t("author"), "author")]
        cidx = 1 if self.data.get("category") == "author" else 0
        self.cat_seg = Segmented(cats, index=cidx)
        base.add_widget(self.cat_seg)

        base.add_widget(Btn(text="🖼  " + t("pick_photo"), bg="surface_alt", fg="text",
                            height=dp(44), size=13, on_press_cb=self._pick_photo))
        self.photo_lbl = TLabel(text=self.photo_path or "—", size=11,
                                color_key="text_muted")
        base.add_widget(self.photo_lbl)
        self.col.add(base)

        # --- параметры
        self.col.add(TLabel(text=t("params"), size=17, bold=True))
        self.params_box = BoxLayout(orientation="vertical", size_hint_y=None,
                                    spacing=dp(10))
        self.params_box.bind(minimum_height=self.params_box.setter("height"))
        self.col.add(self.params_box)
        self.col.add(Btn(text=t("add_param"), bg="surface_alt", fg="text",
                         height=dp(42), size=13, on_press_cb=lambda: self._add_param()))

        # --- шаги
        self.col.add(TLabel(text=t("steps"), size=17, bold=True))
        self.steps_box = BoxLayout(orientation="vertical", size_hint_y=None,
                                   spacing=dp(10))
        self.steps_box.bind(minimum_height=self.steps_box.setter("height"))
        self.col.add(self.steps_box)
        self.col.add(Btn(text=t("add_step"), bg="surface_alt", fg="text",
                         height=dp(42), size=13, on_press_cb=lambda: self._add_step()))

        self.col.add(Btn(text=t("save"), height=dp(52), on_press_cb=self._save))

        # предзаполнение
        for p in self.data.get("params", []):
            self._add_param(p)
        for s in self.data.get("steps", []):
            self._add_step(s)
        if not self.data.get("params"):
            self._add_param()
        if not self.data.get("steps"):
            self._add_step()

    # ------------------------------------------------------------------
    def _add_param(self, data=None):
        data = data or {}
        card = Card(color_key="surface")
        label = Input(hint=t("label"))
        value = Input(hint=t("value"))
        unit = Input(hint=t("unit"))
        lab = data.get("label")
        label.text = lab.get("ru", "") if isinstance(lab, dict) else (lab or "")
        v = data.get("value")
        value.text = "" if v is None else (str(v) if not isinstance(v, list)
                                           else "%s-%s" % (v[0], v[1]))
        if not value.text:
            value.text = data.get("text", {}).get("ru", "") if isinstance(
                data.get("text"), dict) else (data.get("text") or "")
        unit.text = data.get("unit", "")
        card.add_widget(label)
        row = BoxLayout(size_hint_y=None, height=dp(46), spacing=dp(8))
        row.add_widget(value)
        row.add_widget(unit)
        card.add_widget(row)
        card.add_widget(Btn(text=t("delete"), bg="surface_alt", fg="danger",
                            height=dp(36), size=12,
                            on_press_cb=lambda: self._remove(card, self.params_box,
                                                             self.param_rows, entry)))
        entry = {"card": card, "label": label, "value": value, "unit": unit}
        self.param_rows.append(entry)
        self.params_box.add_widget(card)

    def _add_step(self, data=None):
        data = data or {}
        card = Card(color_key="surface")
        title = Input(hint=t("step_title"))
        text = Input(hint=t("step_text"), multiline=True, height=dp(80))
        tip = Input(hint=t("step_tip"))
        timer = Input(hint=t("step_timer"))
        ttl = data.get("title")
        title.text = ttl.get("ru", "") if isinstance(ttl, dict) else (ttl or "")
        txt = data.get("text")
        text.text = txt.get("ru", "") if isinstance(txt, dict) else (txt or "")
        tp = data.get("tip")
        tip.text = tp.get("ru", "") if isinstance(tp, dict) else (tp or "")
        timer.text = str(data.get("timer") or "")
        for w in (title, text, tip, timer):
            card.add_widget(w)
        card.add_widget(Btn(text=t("delete"), bg="surface_alt", fg="danger",
                            height=dp(36), size=12,
                            on_press_cb=lambda: self._remove(card, self.steps_box,
                                                             self.step_rows, entry)))
        entry = {"card": card, "title": title, "text": text, "tip": tip, "timer": timer}
        self.step_rows.append(entry)
        self.steps_box.add_widget(card)

    def _remove(self, card, box, rows, entry):
        if entry in rows:
            rows.remove(entry)
        box.remove_widget(card)

    # ------------------------------------------------------------------
    def _pick_photo(self):
        try:
            from plyer import filechooser
            paths = filechooser.open_file(title=t("pick_photo"),
                                          filters=[["Images", "*.png", "*.jpg", "*.jpeg"]])
            if paths:
                self.photo_path = paths[0]
                self.photo_lbl.text = self.photo_path
                return
        except Exception:
            pass
        chooser = FileChooserIconView(filters=["*.png", "*.jpg", "*.jpeg"])
        popup = Popup(title=t("pick_photo"), content=chooser, size_hint=(0.9, 0.9))

        def _select(*_):
            if chooser.selection:
                self.photo_path = chooser.selection[0]
                self.photo_lbl.text = self.photo_path
            popup.dismiss()

        chooser.bind(on_submit=_select)
        popup.open()

    # ------------------------------------------------------------------
    def _parse_value(self, raw):
        raw = (raw or "").strip().replace(",", ".")
        if not raw:
            return None, None
        if "-" in raw:
            parts = raw.split("-", 1)
            try:
                return [float(parts[0]), float(parts[1])], None
            except ValueError:
                return None, raw
        try:
            return float(raw), None
        except ValueError:
            return None, raw

    def _save(self):
        name = self.name_in.text.strip()
        if not name:
            toast(t("name"))
            return
        params = []
        for i, e in enumerate(self.param_rows):
            label = e["label"].text.strip()
            if not label:
                continue
            value, text = self._parse_value(e["value"].text)
            params.append({
                "key": "p%d" % i,
                "label": {"ru": label, "en": label},
                "value": value,
                "text": {"ru": text, "en": text} if text else None,
                "unit": e["unit"].text.strip(),
                "scale": bool(value is not None and e["unit"].text.strip() in ("g", "ml")),
            })
        steps = []
        for i, e in enumerate(self.step_rows):
            ttl = e["title"].text.strip()
            if not ttl:
                continue
            try:
                timer = int(float(e["timer"].text)) if e["timer"].text.strip() else None
            except ValueError:
                timer = None
            steps.append({
                "n": len(steps) + 1,
                "title": {"ru": ttl, "en": ttl},
                "text": {"ru": e["text"].text.strip(), "en": e["text"].text.strip()},
                "tip": {"ru": e["tip"].text.strip(), "en": e["tip"].text.strip()},
                "timer": timer,
            })
        kind = self.kind_seg.value
        data = {
            "id": self.recipe_id or ("user_%s" % uuid.uuid4().hex[:8]),
            "kind": kind,
            "category": self.cat_seg.value,
            "icon": "☕" if kind == "coffee" else "🍵",
            "name": {"ru": name, "en": name},
            "desc": {"ru": self.desc_in.text.strip(), "en": self.desc_in.text.strip()},
            "photo": self.photo_path,
            "base_servings": 1,
            "servings_options": [1, 2] if kind == "coffee" else [1, 2, 3],
            "params": params,
            "steps": steps,
            "tips": [],
            "is_user": True,
        }
        self.app.store.save_user_recipe(data)
        toast(t("saved"))
        self.app.pop()
