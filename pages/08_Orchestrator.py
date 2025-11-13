
import json, yaml, streamlit as st
from typing import Dict, Any
from core.orchestrator_store import save_orchestration, list_orchestrations, load_orchestration
from core.orchestrator_runtime import run_orchestration, run_step
from core.ipav_shared import list_agent_personas

st.set_page_config(page_title="🧩 Orchestrator", page_icon="🧩")
st.title("🧩 Orchestrator — Multi-Agent / Multi-Recipe")
st.caption("Compose multi-step workflows across agents & recipes. Import/export, test steps, and run end-to-end.")


def example_orchestration(name: str) -> Dict[str,Any]:
    if name.startswith("ServiceNow Connector"):
        return {
            "name": "ServiceNow Connector + Test",
            "globals": {},
            "steps": [
                {"label":"Create Connector","agent":"ActAgent","recipe":"sn_connector","mode":"tool",
                 "tool":"mcp_create_servicenow",
                 "params":{"base_url":"https://YOUR_INSTANCE.service-now.com","user":"YOUR_USER","password":"YOUR_PASSWORD","token":""}},
                {"label":"Health Check","agent":"VerifyAgent","recipe":"sn_health","mode":"tool",
                 "tool":"mcp_test_servicenow","params":{}},
                {"label":"Confirm","agent":"VerifyAgent","recipe":"confirm","mode":"llm",
                 "system":"You confirm ServiceNow connectivity.","developer":"Be concise.",
                 "user":"Connector status: {last}","model":""}
            ]
        }
    if name.startswith("SOP"):
        return {
            "name": "SOP → KB Article (mock or real via secrets)",
            "globals": {"model_default": ""},
            "steps": [
                {"label":"Intake SOP","agent":"IntakeAgent","recipe":"intake_sop","mode":"llm",
                 "system":"You are an Intake Agent. Normalize the SOP content.",
                 "developer":"Return a clean, concise outline of the SOP steps.",
                 "user":"{globals[sop_text] if globals and 'sop_text' in globals else 'Paste SOP here.'}","model":""},
                {"label":"Convert to KB","agent":"PlanAgent","recipe":"kb_convert","mode":"llm",
                 "system":"You convert SOPs into KB articles for ServiceNow.","developer":"Use clear headings and concise language.",
                 "user":"Using the normalized SOP above, draft a KB article body.","model":""},
                {"label":"Publish to ServiceNow","agent":"ActAgent","recipe":"kb_publish","mode":"tool",
                 "tool":"servicenow_publish_kb",
                 "params":{"simulate": True, "title":"KB from SOP", "body":"{last[response] if last and 'response' in last else 'KB body'}"}},
                {"label":"Verify & PDF","agent":"VerifyAgent","recipe":"artifact_capture","mode":"llm",
                 "system":"You verify publishing and summarize results.","developer":"Mention the article URL and attached PDF path if available.",
                 "user":"Summarize the publish result: {last}","model":""}
            ]
        }
    if name.startswith("MCP Create"):
        return {
            "name": "MCP Create + Test Message",
            "globals": {},
            "steps": [
                {"label":"Create MCP (mock)","agent":"ActAgent","recipe":"mcp_create","mode":"tool",
                 "tool":"mcp_create_and_test","params":{"simulate": True, "name":"slack","channel":"#av-ops","message":"Hello from Orchestrator (demo)."}},
                {"label":"Confirm","agent":"VerifyAgent","recipe":"confirm","mode":"llm",
                 "system":"You confirm connector setup.","developer":"","user":"Confirm we created the connector and sent a test: {last}","model":""}
            ]
        }
    return {
        "name": "Baseline YAML → Dashboard metrics",
        "globals": {"baseline_yaml_path": "data/samples/baseline_demo.yaml"},
        "steps": [
            {"label":"Load Baseline (info)","agent":"IntakeAgent","recipe":"load_baseline","mode":"llm",
             "system":"You are analyzing baseline metrics.","developer":"Summarize key fields found.",
             "user":"We will load a baseline YAML from {globals[baseline_yaml_path]} then compute metrics.","model":""},
            {"label":"Compute Metrics","agent":"PlanAgent","recipe":"baseline_compute","mode":"tool",
             "tool":"baseline_dashboard",
             "params":{"baseline": {"incidents_per_month": 150, "minutes_per_incident": 10, "cost_per_minute": 1.4167,
                                    "meetings_per_month": 12000, "avg_participants": 6.2}}},
            {"label":"Render Summary","agent":"VerifyAgent","recipe":"render","mode":"llm",
             "system":"You render a succinct dashboard summary.","developer":"Create a table of key metrics.",
             "user":"Use these metrics: {last}","model":""}
        ]
    }


if "orch" not in st.session_state:
    st.session_state.orch = {"name": "Untitled Orchestration", "globals": {}, "steps": []}

def add_step(default=None):
    st.session_state.orch["steps"].append(default or {
        "label": "Step",
        "agent": "",
        "recipe": "",
        "mode": "llm",
        "system": "",
        "developer": "",
        "user": "",
        "model": "",
        "params": {},
        "halt_on_error": True
    })

def reset(orchestrator=None):
    st.session_state.orch = orchestrator or {"name": "Untitled Orchestration", "globals": {}, "steps": []}

with st.sidebar:
    st.subheader("Import / Export")
    upl = st.file_uploader("Import Orchestration JSON", type=["json"])
    if upl:
        try:
            data = json.loads(upl.read().decode("utf-8"))
            reset(data)
            st.success("Imported orchestration.")
        except Exception as e:
            st.error(f"Import failed: {e}")
    if st.button("Export JSON"):
        st.download_button("Download orchestration.json",
                           data=json.dumps(st.session_state.orch, indent=2).encode("utf-8"),
                           file_name="orchestration.json", mime="application/json")
    st.markdown("---")
    st.subheader("Examples")
    ex = st.selectbox("Load example", ["(none)",
                                       "ServiceNow Connector + Test",
                                       "ServiceNow Connector + Test",
                                       "SOP → KB Article (ServiceNow mock)",
                                       "MCP Create + Test Message",
                                       "Baseline YAML → Dashboard metrics"])
    if st.button("Load Example"):
        if ex != "(none)":
            reset(example_orchestration(ex))
            st.rerun()

    st.markdown("---")
    st.subheader("Saved Orchestrations")
    saved = list_orchestrations()
    if saved:
        names = [f"{s['name']} — {s['id'][:8]}" for s in saved]
        pick = st.selectbox("Load saved", names)
        if st.button("Load Selected"):
            idx = names.index(pick)
            data = load_orchestration(saved[idx]["id"])
            if data:
                reset(data)
                st.success("Loaded from DB.")
                st.rerun()
    else:
        st.caption("No saved orchestrations yet.")

st.session_state.orch["name"] = st.text_input("Label", value=st.session_state.orch.get("name",""))
colA, colB = st.columns(2)
with colA:
    st.session_state.orch["globals"]["model_default"] = st.text_input("Default model (optional)",
                                                                      value=st.session_state.orch["globals"].get("model_default",""))
with colB:
    st.session_state.orch["globals"]["seed"] = st.number_input("Seed", value=int(st.session_state.orch["globals"].get("seed", 42)))

st.markdown("### Steps")
if st.button("➕ Add Step"):
    add_step()

personas = list_agent_personas()
persona_names = [p["name"] for p in personas]

for i, step in enumerate(st.session_state.orch["steps"]):
    with st.container():
        c1, c2 = st.columns([3,1])
        with c1:
            step["label"] = st.text_input("Step Label", key=f"lbl{i}", value=step.get("label","Step"))
        with c2:
            step["mode"] = st.selectbox("Mode", ["llm","tool"], key=f"mode{i}", index=(0 if step.get("mode","llm")=="llm" else 1))

        col1, col2, col3 = st.columns(3)
        with col1:
            options = persona_names + ["(none)"]
            current = step.get("agent") or "(none)"
            idx = options.index(current) if current in options else len(options)-1
            step["agent"] = st.selectbox("Agent", options, key=f"agent{i}", index=idx)
        with col2:
            step["recipe"] = st.text_input("Recipe / Action Name", key=f"recipe{i}", value=step.get("recipe",""))
        with col3:
            step["halt_on_error"] = st.checkbox("Halt on error", key=f"halt{i}", value=bool(step.get("halt_on_error", True)))

        if step["mode"] == "llm":
            step["system"] = st.text_area("System", key=f"sys{i}", value=step.get("system",""))
            step["developer"] = st.text_area("Developer", key=f"dev{i}", value=step.get("developer",""))
            step["user"] = st.text_area("User", key=f"user{i}", value=step.get("user",""))
            step["model"] = st.text_input("Model override (optional)", key=f"model{i}", value=step.get("model",""))
        else:
            params_text = st.text_area("Tool Params (JSON)", key=f"params{i}", value=json.dumps(step.get("params", {}), indent=2))
            try:
                step["params"] = json.loads(params_text)
            except Exception:
                st.warning("Params are not valid JSON.")

        cc = st.columns([1,1,1,1])
        with cc[0]:
            if st.button("Test Step", key=f"test{i}"):
                ok, out = run_step(step, {"globals": st.session_state.orch.get("globals",{}), "last": None})
                if ok:
                    st.success("Step OK")
                    st.json(out)
                else:
                    st.error("Step failed")
                    st.json(out)
        with cc[1]:
            if st.button("Delete", key=f"del{i}"):
                st.session_state.orch["steps"].pop(i)
                st.rerun()
        with cc[2]:
            if st.button("↑ Move Up", key=f"up{i}") and i>0:
                st.session_state.orch["steps"][i-1], st.session_state.orch["steps"][i] = st.session_state.orch["steps"][i], st.session_state.orch["steps"][i-1]
                st.rerun()
        with cc[3]:
            if st.button("↓ Move Down", key=f"down{i}") and i < len(st.session_state.orch["steps"])-1:
                st.session_state.orch["steps"][i+1], st.session_state.orch["steps"][i] = st.session_state.orch["steps"][i], st.session_state.orch["steps"][i+1]
                st.rerun()

st.markdown("---")
run_cols = st.columns([1,1,2])
with run_cols[0]:
    if st.button("▶️ Run Orchestration"):
        result = run_orchestration(st.session_state.orch)
        if result.get("ok"):
            st.success("Run complete")
        else:
            st.error(f"Failed on step {result.get('error_step')}")
        st.json(result)
with run_cols[1]:
    if st.button("💾 Save Orchestration"):
        oid = save_orchestration(st.session_state.orch["name"], st.session_state.orch)
        st.success(f"Saved (id: {oid[:8]}…)")

def example_orchestration(name: str) -> Dict[str,Any]:

    if name.startswith("ServiceNow Connector"):
        return {
            "name": "ServiceNow Connector + Test",
            "globals": {},
            "steps": [
                {"label":"Create Connector","agent":"ActAgent","recipe":"sn_connector","mode":"tool",
                 "tool":"mcp_create_servicenow",
                 "params":{"base_url":"https://YOUR_INSTANCE.service-now.com","user":"YOUR_USER","password":"YOUR_PASSWORD","token":""}},
                {"label":"Health Check","agent":"VerifyAgent","recipe":"sn_health","mode":"tool",
                 "tool":"mcp_test_servicenow","params":{}},
                {"label":"Confirm","agent":"VerifyAgent","recipe":"confirm","mode":"llm",
                 "system":"You confirm ServiceNow connectivity.","developer":"Be concise.",
                 "user":"Connector status: {last}","model":""}
            ]
        }

    if name.startswith("SOP"):
        return {
            "name": "SOP → KB Article (mock)",
            "globals": {"model_default": ""},
            "steps": [
                {"label":"Intake SOP","agent":"IntakeAgent","recipe":"intake_sop","mode":"llm",
                 "system":"You are an Intake Agent. Normalize the SOP content.",
                 "developer":"Return a clean, concise outline of the SOP steps.",
                 "user":"{globals[sop_text] if globals and 'sop_text' in globals else 'Paste SOP here.'}","model":""},
                {"label":"Convert to KB","agent":"PlanAgent","recipe":"kb_convert","mode":"llm",
                 "system":"You convert SOPs into KB articles for ServiceNow.","developer":"Use clear headings and concise language.",
                 "user":"Using the normalized SOP above, draft a KB article body.","model":""},
                {"label":"Publish to ServiceNow","agent":"ActAgent","recipe":"kb_publish","mode":"tool",
                 "tool":"servicenow_publish_kb","params":{"simulate": True, "title":"KB from SOP", "body":"{last[response] if last and 'response' in last else 'KB body'}"}},
                {"label":"Verify & PDF","agent":"VerifyAgent","recipe":"artifact_capture","mode":"llm",
                 "system":"You verify publishing and summarize results.","developer":"Mention the article URL and attached PDF path if available.",
                 "user":"Summarize the publish result: {last}","model":""}
            ]
        }
    if name.startswith("MCP"):
        return {
            "name": "MCP Create + Test Message",
            "globals": {},
            "steps": [
                {"label":"Create MCP (mock)","agent":"ActAgent","recipe":"mcp_create","mode":"tool",
                 "tool":"mcp_create_and_test","params":{"simulate": True, "name":"slack","channel":"#av-ops","message":"Hello from Orchestrator (demo)."}},
                {"label":"Confirm","agent":"VerifyAgent","recipe":"confirm","mode":"llm",
                 "system":"You confirm connector setup.","developer":"","user":"Confirm we created the connector and sent a test: {last}","model":""}
            ]
        }
    return {
        "name": "Baseline YAML → Dashboard metrics",
        "globals": {"baseline_yaml_path": "data/samples/baseline_demo.yaml"},
        "steps": [
            {"label":"Load Baseline (info)","agent":"IntakeAgent","recipe":"load_baseline","mode":"llm",
             "system":"You are analyzing baseline metrics.","developer":"Summarize key fields found.",
             "user":"We will load a baseline YAML from {globals[baseline_yaml_path]} then compute metrics.","model":""},
            {"label":"Compute Metrics","agent":"PlanAgent","recipe":"baseline_compute","mode":"tool",
             "tool":"baseline_dashboard",
             "params":{"baseline": {"incidents_per_month": 150, "minutes_per_incident": 10, "cost_per_minute": 1.4167,
                                    "meetings_per_month": 12000, "avg_participants": 6.2}}},
            {"label":"Render Summary","agent":"VerifyAgent","recipe":"render","mode":"llm",
             "system":"You render a succinct dashboard summary.","developer":"Create a table of key metrics.",
             "user":"Use these metrics: {last}","model":""}
        ]
    }
