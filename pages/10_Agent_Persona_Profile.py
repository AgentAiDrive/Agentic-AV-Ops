
# 10_Agent_Persona_Profile.py
import json, textwrap
import streamlit as st
from core.ipav_shared import AgentPersona, save_agent_persona, list_agent_personas

st.set_page_config(page_title="Agent Persona & Profile", page_icon="🧩")

st.title("🧩 Agent Persona & Profile Builder")

with st.expander("What is this?"):
    st.markdown("""
    Define an **Agent persona** (role, domain, tone, tools, constraints) and generate a standardized **system prompt**.
    Saved personas can be reused by the Chat and Prompt Generator pages.
    """)

with st.form("persona_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Agent Name*", value=st.session_state.get("persona_name",""))
        role = st.text_input("Role / Title", value="AV/UC Operations Agent")
        domain = st.text_input("Domain / Expertise", value="Enterprise AV, Conference Rooms, Zoom/Teams")
        tone = st.text_input("Tone", value="Concise, actionable, audit-friendly")
    with col2:
        tools = st.text_area("Tools (comma-separated)", value="ServiceNow, Slack, Zoom, Teams, Q-SYS, Extron")
        inputs = st.text_area("Expected Inputs", value="SOP text, incidents, room IDs, device models")
        outputs = st.text_area("Expected Outputs", value="Recipes (YAML/JSON), KB articles, tickets, status updates")
    goals = st.text_area("Goals", value="Convert SOPs into agentic recipes and workflows; reduce MTTR; improve on-time starts")
    constraints = st.text_area("Constraints / Guardrails", value="No secrets in output; verifiable steps; include evidence capture")
    meta = st.text_area("Optional metadata (JSON)", value="{}", help="Any extra metadata you want to attach")
    generate = st.form_submit_button("Generate & Save Persona")

if generate:
    # Build system prompt
    sys_prompt = textwrap.dedent(f"""
    You are **{role}** operating in **{domain}**.
    Tone: {tone}
    Goals: {goals}
    Constraints: {constraints}
    Tools available: {tools}
    Inputs: {inputs}
    Outputs: {outputs}
    Respond with precise, step-by-step actions and structured results (JSON or YAML) when appropriate.
    """).strip()

    try:
        metadata_json = json.dumps(json.loads(meta), ensure_ascii=False)
    except Exception:
        metadata_json = json.dumps({"raw": meta}, ensure_ascii=False)

    ap = AgentPersona(
        name=name, role=role, domain=domain, tone=tone, goals=goals,
        constraints=constraints, tools=tools, inputs=inputs, outputs=outputs,
        system_prompt=sys_prompt, metadata_json=metadata_json
    )
    persona_id = save_agent_persona(ap)
    st.success(f"Saved persona '{name}' (id: {persona_id[:8]}…).")
    st.code(sys_prompt, language="markdown")

st.subheader("Saved Personas")
rows = list_agent_personas()
if rows:
    for r in rows[:10]:
        with st.container(border=True):
            st.markdown(f"**{r['name']}** — _{r['role']}_")
            with st.expander("Preview system prompt"):
                st.code(r["system_prompt"], language="markdown")
else:
    st.info("No personas saved yet. Create one above.")
