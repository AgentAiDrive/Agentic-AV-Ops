
from __future__ import annotations
import os, json, time, base64
from typing import Dict, Any, Tuple
import requests

from core.ipav_shared import call_llm

# -------- ServiceNow auth helpers --------
def _sn_from_params_or_secrets(params: Dict[str,Any]) -> Dict[str,str]:
    base_url = params.get("base_url") or ""
    token = params.get("token") or ""
    user = params.get("user") or ""
    password = params.get("password") or ""
    api_key = params.get("api_key") or ""
    user_token = params.get("user_token") or ""

    # Try Streamlit secrets if not provided
    try:
        import streamlit as st  # type: ignore
        sect = st.secrets.get("servicenow", {})
        base_url = base_url or sect.get("base_url", "")
        token = token or sect.get("token", "")
        user = user or sect.get("user", "")
        password = password or sect.get("password", "")
        api_key = api_key or sect.get("api_key", "")
        user_token = user_token or sect.get("user_token", "")
    except Exception:
        pass

    # Fallback env vars
    base_url = base_url or os.getenv("SERVICENOW_BASE_URL", "")
    token = token or os.getenv("SERVICENOW_TOKEN", "")
    user = user or os.getenv("SERVICENOW_USER", "")
    password = password or os.getenv("SERVICENOW_PASSWORD", "")
    api_key = api_key or os.getenv("SERVICENOW_API_KEY", "")
    user_token = user_token or os.getenv("SERVICENOW_USER_TOKEN", "")

    return {"base_url": base_url, "token": token, "user": user, "password": password, "api_key": api_key, "user_token": user_token}

def _sn_headers(auth: Dict[str,str]) -> Dict[str,str]:
    h = {"Accept": "application/json", "Content-Type": "application/json"}
    # Prefer Bearer token if provided
    if auth.get("token"):
        h["Authorization"] = f"Bearer {auth['token']}"
    # Some instances use custom headers
    if auth.get("api_key"):
        h["X-API-Key"] = auth["api_key"]
    if auth.get("user_token"):
        h["X-UserToken"] = auth["user_token"]
    return h

def _sn_auth_tuple(auth: Dict[str,str]):
    if auth.get("token"):
        return None  # using Bearer header
    if auth.get("user") and auth.get("password"):
        return (auth["user"], auth["password"])  # basic auth
    return None

# -------- Orchestration runner --------
def run_orchestration(orch: Dict[str,Any]) -> Dict[str,Any]:
    ctx: Dict[str,Any] = {"globals": orch.get("globals", {}), "steps": [], "started_at": time.time()}
    for idx, step in enumerate(orch.get("steps", [])):
        ok, out = run_step(step, ctx)
        ctx["steps"].append({"index": idx, "ok": ok, "output": out})
        ctx["last"] = out
        if not ok and step.get("halt_on_error", True):
            return {"ok": False, "error_step": idx, "context": ctx}
    ctx["finished_at"] = time.time()
    return {"ok": True, "context": ctx}

def run_step(step: Dict[str,Any], ctx: Dict[str,Any]) -> Tuple[bool, Any]:
    mode = step.get("mode", "llm")
    if mode == "llm":
        system = (step.get("system") or "").format(**safe_ctx(ctx))
        developer = (step.get("developer") or "").format(**safe_ctx(ctx))
        user = (step.get("user") or "").format(**safe_ctx(ctx))
        prompt = (f"[DEV]\\n{developer}\\n\\n" if developer else "") + user
        try:
            resp = call_llm(prompt, system=system, model=step.get("model"))
            return True, {"type": "llm", "response": resp}
        except Exception as e:
            return False, {"type": "llm", "error": str(e)}
    elif mode == "tool":
        tool = step.get("tool", "")
        params = step.get("params", {}) or {}
        try:
            out = run_tool(tool, params, ctx)
            return True, {"type": "tool", "tool": tool, "result": out}
        except Exception as e:
            return False, {"type": "tool", "tool": tool, "error": str(e)}
    else:
        return False, {"error": f"Unknown mode: {mode}"}

def safe_ctx(ctx: Dict[str,Any]) -> Dict[str,Any]:
    last = ctx.get("last")
    return {"last": last if isinstance(last, (dict, list, str, int, float)) else str(last),
            "globals": ctx.get("globals", {})}

# -------- Tool implementations (real ServiceNow + mocks) --------
def run_tool(tool: str, params: Dict[str,Any], ctx: Dict[str,Any]) -> Any:
    simulate = params.get("simulate", False)

    if tool == "servicenow_health":
        if simulate:
            return {"ok": True, "simulate": True}
        auth = _sn_from_params_or_secrets(params)
        base = auth["base_url"].rstrip("/")
        if not base:
            raise RuntimeError("Missing ServiceNow base_url (secret or params).")
        r = requests.get(f"{base}/api/now/table/sys_user?sysparm_limit=1",
                         headers=_sn_headers(auth), auth=_sn_auth_tuple(auth), timeout=20)
        r.raise_for_status()
        data = r.json()
        return {"ok": True, "sample": data}

    if tool == "servicenow_publish_kb":
        # Create a KB article; try to return a PDF (fallback to minimal PDF if feature not enabled)
        title = params.get("title", "KB Article")
        body = params.get("body", "No content")
        kb_sys_id = params.get("knowledge_base")  # optional sys_id
        fetch_pdf = bool(params.get("fetch_pdf", True))

        if simulate:
            pdf_path = _write_minimal_pdf(f"{title}\n\n{body[:2000]}")
            art_id = f"KB{int(time.time())}"
            return {"article_id": art_id, "url": f"https://example.service-now.com/kb/{art_id}", "pdf": pdf_path, "simulate": True}

        auth = _sn_from_params_or_secrets(params)
        base = auth["base_url"].rstrip("/")
        if not base:
            raise RuntimeError("Missing ServiceNow base_url (secret or params).")

        payload = {
            "short_description": title,
            "text": body
        }
        if kb_sys_id:
            payload["knowledge_base"] = kb_sys_id

        r = requests.post(f"{base}/api/now/table/kb_knowledge",
                          headers=_sn_headers(auth), auth=_sn_auth_tuple(auth),
                          json=payload, timeout=30)
        r.raise_for_status()
        res = r.json()
        article_sys_id = res.get("result", {}).get("sys_id")
        url = f"{base}/kb_knowledge.do?sys_id={article_sys_id}" if article_sys_id else f"{base}/kb_find.do"

        pdf_path = None
        if fetch_pdf:
            try:
                # Not all instances expose PDF export; fallback to minimal PDF
                pdf_path = _write_minimal_pdf(f"{title}\n\n{body[:2000]}")
            except Exception:
                pdf_path = _write_minimal_pdf(f"{title}\n\n{body[:2000]}")

        return {"article_sys_id": article_sys_id, "url": url, "pdf": pdf_path}

    if tool == "mcp_create_servicenow":
        # Save connector creds for reuse (file + env for this session)
        cfg = {
            "base_url": params.get("base_url", ""),
            "user": params.get("user", ""),
            "password": params.get("password", ""),
            "token": params.get("token", ""),
        }
        # Prefer secrets; but persist locally to file for demo reuse
        path = os.path.abspath("servicenow_conn.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        # Also set env for current process
        if cfg["base_url"]: os.environ["SERVICENOW_BASE_URL"] = cfg["base_url"]
        if cfg["user"]: os.environ["SERVICENOW_USER"] = cfg["user"]
        if cfg["password"]: os.environ["SERVICENOW_PASSWORD"] = cfg["password"]
        if cfg["token"]: os.environ["SERVICENOW_TOKEN"] = cfg["token"]
        return {"saved": True, "path": path, "note": "For production, prefer Streamlit secrets."}

    if tool == "mcp_test_servicenow":
        # Load from file if present, else rely on secrets/env; hit a simple endpoint
        path = os.path.abspath("servicenow_conn.json")
        params = dict(params)  # copy
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                for k,v in cfg.items():
                    params.setdefault(k, v)
            except Exception:
                pass
        if simulate:
            return {"ok": True, "simulate": True}
        auth = _sn_from_params_or_secrets(params)
        base = auth["base_url"].rstrip("/")
        if not base:
            raise RuntimeError("Missing ServiceNow base_url (secret or params).")
        r = requests.get(f"{base}/api/now/table/sys_user?sysparm_limit=1",
                         headers=_sn_headers(auth), auth=_sn_auth_tuple(auth), timeout=20)
        r.raise_for_status()
        return {"ok": True, "status": r.status_code}

    if tool == "baseline_dashboard":
        baseline = params.get("baseline") or {}
        cost_per_min = max(0.0, float(baseline.get("cost_per_minute", 0)))
        incidents = float(baseline.get("incidents_per_month", 0))
        minutes_per_incident = float(baseline.get("minutes_per_incident", 10))
        minutes_lost = incidents * minutes_per_incident
        cost_impact = minutes_lost * cost_per_min
        return {
            "minutes_lost": minutes_lost,
            "cost_per_minute": cost_per_min,
            "cost_impact": round(cost_impact, 2),
            "meetings_per_month": baseline.get("meetings_per_month"),
            "avg_participants": baseline.get("avg_participants"),
            "notes": "Demo computation; replace with real baseline."
        }

    raise RuntimeError(f"Unknown tool: {tool}")

def _write_minimal_pdf(text: str) -> str:
    safe = text.replace("(", "[").replace(")", "]").replace("\\", "/")
    content = f"""%PDF-1.1
1 0 obj<<>>endobj
2 0 obj<< /Length 44 >>stream
BT /F1 12 Tf 72 720 Td ({safe[:200]}) Tj ET
endstream endobj
3 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj
4 0 obj<< /Type /Page /Parent 5 0 R /Resources << /Font << /F1 3 0 R >> >> /Contents 2 0 R /MediaBox [0 0 612 792] >>endobj
5 0 obj<< /Type /Pages /Kids [4 0 R] /Count 1 >>endobj
6 0 obj<< /Type /Catalog /Pages 5 0 R >>endobj
xref
0 7
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000171 00000 n 
0000000255 00000 n 
0000000398 00000 n 
0000000453 00000 n 
trailer<< /Root 6 0 R /Size 7 >>
startxref
510
%%EOF
"""
    out_path = os.path.abspath(os.path.join(os.getcwd(), f"kb_article_{int(time.time())}.pdf"))
    with open(out_path, "wb") as f:
        f.write(content.encode("latin-1", "ignore"))
    return out_path
