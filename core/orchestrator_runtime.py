
from __future__ import annotations
import os, json, base64, time
from typing import Dict, Any, Tuple, Optional, List

from core.ipav_shared import call_llm

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
        prompt = ""
        if developer:
            prompt += f"[DEV]\n{developer}\n\n"
        prompt += user
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

def run_tool(tool: str, params: Dict[str,Any], ctx: Dict[str,Any]) -> Any:
    simulate = params.get("simulate", True)
    if tool == "servicenow_publish_kb":
        title = params.get("title", "KB Article")
        body = params.get("body", "No content")
        article_id = f"KB{int(time.time())}"
        pdf_path = params.get("pdf_path") or _write_minimal_pdf(f"{title}\n\n{body[:500]}")
        return {"article_id": article_id, "url": f"https://example.service-now.com/kb/{article_id}", "pdf": pdf_path, "simulate": simulate}
    if tool == "mcp_create_and_test":
        tool_name = params.get("name", "slack")
        channel = params.get("channel", "#general")
        message = params.get("message", "Hello from Orchestrator (demo).")
        return {"created": True, "tool": tool_name, "test_send": {"channel": channel, "message": message, "status": "ok"}, "simulate": simulate}
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
