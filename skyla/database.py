from __future__ import annotations
import sqlite3, threading
from datetime import datetime, timezone
from pathlib import Path

class Database:
    def __init__(self, path: Path): self.path, self._lock = path, threading.RLock(); self.initialize()
    def connect(self):
        c=sqlite3.connect(self.path, check_same_thread=False); c.row_factory=sqlite3.Row; return c
    def initialize(self):
        with self.connect() as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, category TEXT NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, UNIQUE(category,key));
CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, user_input TEXT, intent TEXT, confidence REAL, module TEXT, model TEXT, action TEXT, result TEXT, latency_ms REAL, error TEXT);
CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, due_at TEXT, status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);''')
    def remember(self, key, value, category="facts"):
        now=datetime.now(timezone.utc).isoformat()
        with self._lock, self.connect() as c: c.execute("INSERT INTO memory(category,key,value,created_at,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(category,key) DO UPDATE SET value=excluded.value,updated_at=excluded.updated_at",(category,key,value,now,now))
    def search_memory(self, query="", category=None):
        sql="SELECT * FROM memory WHERE (key LIKE ? OR value LIKE ?)"; args=[f"%{query}%",f"%{query}%"]
        if category: sql += " AND category=?"; args.append(category)
        with self.connect() as c: return [dict(r) for r in c.execute(sql+" ORDER BY updated_at DESC",args)]
    def forget(self, key):
        with self._lock, self.connect() as c: return c.execute("DELETE FROM memory WHERE key=?",(key,)).rowcount
    def log(self, **kw):
        fields="created_at,user_input,intent,confidence,module,model,action,result,latency_ms,error"; values=[datetime.now(timezone.utc).isoformat()]+[kw.get(x) for x in fields.split(',')[1:]]
        with self._lock, self.connect() as c: c.execute(f"INSERT INTO logs({fields}) VALUES({','.join('?'*len(values))})",values)
    def logs(self, limit=100):
        with self.connect() as c: return [dict(r) for r in c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?",(limit,))]
