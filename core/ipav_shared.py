
# ipav_shared.py
# Lightweight helpers to integrate with an existing IPAV Streamlit app.
from __future__ import annotations
import os, sqlite3, json, time, uuid
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List

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
    CREATE TABLE IF NOT EXISTS agents_persona (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        domain TEXT,
        tone TEXT,
        goals TEXT,
        constraints TEXT,
        tools TEXT,
        inputs TEXT,
        outputs TEXT,
        system_prompt TEXT,
        metadata_json TEXT,
        created_at REAL,
        updated_at REAL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS shortcuts (
        id TEXT PRIMARY KEY,
        label TEXT NOT NULL,
        description TEXT,
        template_json TEXT,
        instructions TEXT,
        format TEXT,
        verbosity TEXT,
        reasoning TEXT,
        created_at REAL,
        updated_at REAL
    );
    """)
    conn.commit()
    conn.close()

def _ts():
    return time.time()

@dataclass
class AgentPersona:
    name: str
    role: str = ""
    domain: str = ""
    tone: str = ""
    goals: str = ""
    constraints: str = ""
    tools: str = ""
    inputs: str = ""
    outputs: str = ""
    system_prompt: str = ""
    metadata_json: str = ""

def save_agent_persona(p: AgentPersona, *, id: Optional[str]=None) -> str:
    ensure_tables()
    id = id or str(uuid.uuid4())
    conn = _connect()
    conn.execute("""
    INSERT OR REPLACE INTO agents_persona
    (id, name, role, domain, tone, goals, constraints, tools, inputs, outputs, system_prompt, metadata_json, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM agents_persona WHERE id=?), ?), ?)
    """, (
        id, p.name, p.role, p.domain, p.tone, p.goals, p.constraints, p.tools, p.inputs, p.outputs, p.system_prompt, p.metadata_json,
        id, _ts(), _ts()
    ))
    conn.commit()
    conn.close()
    return id

def list_agent_personas() -> List[Dict[str,Any]]:
    ensure_tables()
    conn = _connect()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, name, role, domain, tone, system_prompt FROM agents_persona ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "domain": r[3], "tone": r[4], "system_prompt": r[5]} for r in rows]

def get_agent_persona(id: str) -> Optional[Dict[str,Any]]:
    ensure_tables()
    conn = _connect()
    cur = conn.cursor()
    row = cur.execute("""SELECT id, name, role, domain, tone, goals, constraints, tools, inputs, outputs, system_prompt, metadata_json
                         FROM agents_persona WHERE id=?""", (id,)).fetchone()
    conn.close()
    if not row:
        return None
    keys = ["id","name","role","domain","tone","goals","constraints","tools","inputs","outputs","system_prompt","metadata_json"]
    return {k:v for k,v in zip(keys,row)}

def save_shortcut(d: Dict[str,Any], *, id: Optional[str]=None) -> str:
    ensure_tables()
    id = id or str(uuid.uuid4())
    conn = _connect()
    conn.execute("""
    INSERT OR REPLACE INTO shortcuts
    (id, label, description, template_json, instructions, format, verbosity, reasoning, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, COALESCE((SELECT created_at FROM shortcuts WHERE id=?), ?), ?)
    """, (
        id, d.get("Label",""), d.get("Description",""), json.dumps(d.get("Template",{}), ensure_ascii=False),
        d.get("Instructions",""), d.get("Format",""), d.get("Verbosity",""), d.get("Reasoning",""),
        id, _ts(), _ts()
    ))
    conn.commit()
    conn.close()
    return id

def list_shortcuts() -> List[Dict[str,Any]]:
    ensure_tables()
    conn = _connect()
    rows = conn.execute("""SELECT id, label, description, format, verbosity, reasoning, template_json
                           FROM shortcuts ORDER BY updated_at DESC""").fetchall()
    conn.close()
    out = []
    for r in rows:
        out.append({
            "id": r[0], "label": r[1], "description": r[2],
            "format": r[3], "verbosity": r[4], "reasoning": r[5],
            "template": json.loads(r[6] or "{}")
        })
    return out

# --------- LLM dispatch (tries to reuse app providers if available) ---------
def call_llm(prompt: str, *, system: str = "", model: Optional[str]=None) -> str:
    """
    Try to reuse existing app providers if installed; otherwise returns a stubbed echo.
    Expected provider modules (optional):
      - core.llm.providers.openai_client with function completions(prompt, system=None, model=None)
      - core.llm.providers.anthropic_client with function completions(prompt, system=None, model=None)
    """
    try:
        # Prefer app's OpenAI client if present
        from core.llm.providers import openai_client as _oc  # type: ignore
        return _oc.completions(prompt=prompt, system=system, model=model)  # pragma: no cover
    except Exception:
        pass
    try:
        from core.llm.providers import anthropic_client as _ac  # type: ignore
        return _ac.completions(prompt=prompt, system=system, model=model)  # pragma: no cover
    except Exception:
        pass
    # Fallback: deterministic echo for offline/demo
    header = f"[SYSTEM]\n{system}\n\n" if system else ""
    return header + f"[RESPONSE]\nEcho:\n{prompt[:2000]}"
