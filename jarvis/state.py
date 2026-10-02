from __future__ import annotations
import sqlite3
import threading
from pathlib import Path
from typing import Iterable

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,
  profile TEXT NOT NULL,
  model TEXT NOT NULL,
  usage_anchor INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  token_count INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(session_id) REFERENCES sessions(id)
);
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
  content, content='messages', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
  INSERT INTO messages_fts(rowid, content) VALUES (new.id, new.content);
END;
CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
  INSERT INTO messages_fts(messages_fts, rowid, content) VALUES('delete', old.id, old.content);
END;
CREATE TABLE IF NOT EXISTS checkpoints (
  id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  state_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS telemetry (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

class StateStore:
    def __init__(self, path: str):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._init()

    def _conn(self):
        c = sqlite3.connect(self.path, timeout=30, check_same_thread=False)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")
        return c

    def _init(self):
        with self._conn() as c:
            c.executescript(SCHEMA)

    def upsert_session(self, session_id: str, profile: str, model: str):
        with self._lock, self._conn() as c:
            c.execute("""INSERT INTO sessions(id,profile,model) VALUES(?,?,?)
                         ON CONFLICT(id) DO UPDATE SET updated_at=CURRENT_TIMESTAMP""",
                      (session_id, profile, model))

    def set_anchor(self, session_id: str, tokens: int):
        with self._lock, self._conn() as c:
            c.execute("UPDATE sessions SET usage_anchor=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
                      (tokens, session_id))

    def get_anchor(self, session_id: str) -> int:
        with self._conn() as c:
            row=c.execute("SELECT usage_anchor FROM sessions WHERE id=?", (session_id,)).fetchone()
            return int(row["usage_anchor"]) if row else 0

    def add_message(self, session_id: str, role: str, content: str, tokens: int):
        with self._lock, self._conn() as c:
            c.execute("INSERT INTO messages(session_id,role,content,token_count) VALUES(?,?,?,?)",
                      (session_id, role, content, tokens))

    def recent_messages(self, session_id: str, limit: int = 100):
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit)
            ).fetchall()][::-1]

    def search_messages(self, query: str, limit: int = 20):
        with self._conn() as c:
            return [dict(r) for r in c.execute("""
                SELECT m.* FROM messages_fts f
                JOIN messages m ON m.id=f.rowid
                WHERE messages_fts MATCH ?
                ORDER BY m.id DESC LIMIT ?
            """, (query, limit)).fetchall()]

    def checkpoint(self, checkpoint_id: str, session_id: str, state_json: str):
        with self._lock, self._conn() as c:
            c.execute("INSERT OR REPLACE INTO checkpoints(id,session_id,state_json) VALUES(?,?,?)",
                      (checkpoint_id, session_id, state_json))

    def log(self, event: str, payload_json: str):
        with self._lock, self._conn() as c:
            c.execute("INSERT INTO telemetry(event,payload_json) VALUES(?,?)", (event,payload_json))
