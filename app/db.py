# -*- coding: utf-8 -*-
"""Локальная база данных: SQLite (stdlib). Работает полностью офлайн."""

import json
import os
import sqlite3
import time

from app.models import Recipe

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS favorites (
    recipe_id TEXT PRIMARY KEY,
    added_at  REAL
);
CREATE TABLE IF NOT EXISTS notes (
    recipe_id TEXT PRIMARY KEY,
    text      TEXT,
    updated_at REAL
);
CREATE TABLE IF NOT EXISTS user_recipes (
    id         TEXT PRIMARY KEY,
    payload    TEXT,
    updated_at REAL
);
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

DEFAULT_SETTINGS = {
    "theme": "dark",
    "units": "metric",
    "lang": "ru",
}


class Storage(object):
    def __init__(self, db_path, seed_json):
        self.db_path = db_path
        self.seed_json = seed_json
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()
        self._builtin = []
        self._load_builtin()

    # ---- встроенные рецепты (офлайн JSON) -------------------------------
    def _load_builtin(self):
        with open(self.seed_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._builtin = [Recipe(r) for r in data.get("recipes", [])]
        # отметка о первом запуске (для миграций/статистики)
        if not self.get_meta("seeded"):
            self.set_meta("seeded", str(int(time.time())))

    # ---- мета/настройки --------------------------------------------------
    def get_meta(self, key, default=None):
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def set_meta(self, key, value):
        self.conn.execute("REPLACE INTO meta(key, value) VALUES (?,?)", (key, value))
        self.conn.commit()

    def get_settings(self):
        out = dict(DEFAULT_SETTINGS)
        for row in self.conn.execute("SELECT key, value FROM settings"):
            out[row["key"]] = row["value"]
        return out

    def set_setting(self, key, value):
        self.conn.execute("REPLACE INTO settings(key, value) VALUES (?,?)", (key, str(value)))
        self.conn.commit()

    # ---- рецепты ---------------------------------------------------------
    def user_recipes(self):
        out = []
        for row in self.conn.execute("SELECT payload FROM user_recipes ORDER BY updated_at DESC"):
            data = json.loads(row["payload"])
            data["is_user"] = True
            out.append(Recipe(data))
        return out

    def all_recipes(self):
        return list(self._builtin) + self.user_recipes()

    def recipes(self, kind=None, category=None):
        res = self.all_recipes()
        if kind:
            res = [r for r in res if r.kind == kind]
        if category:
            res = [r for r in res if r.category == category]
        return res

    def get_recipe(self, recipe_id):
        for r in self.all_recipes():
            if r.id == recipe_id:
                return r
        return None

    def save_user_recipe(self, data):
        data = dict(data)
        data["is_user"] = True
        self.conn.execute(
            "REPLACE INTO user_recipes(id, payload, updated_at) VALUES (?,?,?)",
            (data["id"], json.dumps(data, ensure_ascii=False), time.time()))
        self.conn.commit()

    def delete_user_recipe(self, recipe_id):
        self.conn.execute("DELETE FROM user_recipes WHERE id=?", (recipe_id,))
        self.conn.execute("DELETE FROM favorites WHERE recipe_id=?", (recipe_id,))
        self.conn.execute("DELETE FROM notes WHERE recipe_id=?", (recipe_id,))
        self.conn.commit()

    # ---- избранное -------------------------------------------------------
    def is_favorite(self, recipe_id):
        row = self.conn.execute(
            "SELECT 1 FROM favorites WHERE recipe_id=?", (recipe_id,)).fetchone()
        return row is not None

    def toggle_favorite(self, recipe_id):
        if self.is_favorite(recipe_id):
            self.conn.execute("DELETE FROM favorites WHERE recipe_id=?", (recipe_id,))
            self.conn.commit()
            return False
        self.conn.execute("REPLACE INTO favorites(recipe_id, added_at) VALUES (?,?)",
                          (recipe_id, time.time()))
        self.conn.commit()
        return True

    def favorites(self, sort="date"):
        rows = self.conn.execute(
            "SELECT recipe_id, added_at FROM favorites ORDER BY added_at DESC").fetchall()
        by_id = {r.id: r for r in self.all_recipes()}
        items = [(by_id[row["recipe_id"]], row["added_at"])
                 for row in rows if row["recipe_id"] in by_id]
        if sort == "alpha":
            items.sort(key=lambda p: p[0].name.lower())
        return [p[0] for p in items]

    # ---- заметки ---------------------------------------------------------
    def get_note(self, recipe_id):
        row = self.conn.execute(
            "SELECT text FROM notes WHERE recipe_id=?", (recipe_id,)).fetchone()
        return row["text"] if row else ""

    def set_note(self, recipe_id, text):
        self.conn.execute("REPLACE INTO notes(recipe_id, text, updated_at) VALUES (?,?,?)",
                          (recipe_id, text, time.time()))
        self.conn.commit()
