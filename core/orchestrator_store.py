from __future__ import annotations
import os, sqlite3, time, uuid, json
from typing import List, Dict, Any, Optional

DB_PATH = os.getenv("IPAV_DB_PATH") or os.path.abspath(os.path.join(os.getcwd(), "avops.db"))

def _connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def ensure_tables():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orchestrations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        json TEXT NOT NULL,
        created_at REAL,
        updated_at REAL
    );
    """)
    conn.commit()
    conn.close()

def save_orchestration(name: str, data: Dict[str,Any], *, id: Optional[str]=None) -> str:
    ensure_tables()
    id = id or str(uuid.uuid4())
    conn = _connect()
    js = json.dumps(data, ensure_ascii=False)
    conn.execute("""
    INSERT OR REPLACE INTO orchestrations
    (id, name, json, created_at, updated_at)
    VALUES (?, ?, ?, COALESCE((SELECT created_at FROM orchestrations WHERE id=?), strftime('%s','now')), strftime('%s','now'))
    """, (id, name, js, id))
    conn.commit()
    conn.close()
    return id

def list_orchestrations() -> List[Dict[str,Any]]:
    ensure_tables()
    conn = _connect()
    rows = conn.execute("SELECT id,name,updated_at FROM orchestrations ORDER BY updated_at DESC").fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({"id": r[0], "name": r[1], "updated_at": r[2]})
    return out

def load_orchestration(id: str) -> Optional[Dict[str,Any]]:
    ensure_tables()
    conn = _connect()
    row = conn.execute("SELECT json FROM orchestrations WHERE id=?", (id,)).fetchone()
    conn.close()
    if not row: return None
    import json as _json
    try:
        return _json.loads(row[0])
    except Exception:
        return None
