
# 11_Prompt_Generator.py
import json, textwrap
import streamlit as st
from core.ipav_shared import list_agent_personas

st.set_page_config(page_title="Prompt Generator", page_icon="🧪")
st.title("🧪 Prompt Generator")

personas = list_agent_personas()
persona_map = {p["name"]: p for p in personas}
choice = st.selectbox("Persona (optional)", ["(none)"] + list(persona_map.keys()))

col1, col2 = st.columns(2)
with col1:
    task = st.text_area("Task / Instruction", value="Transform the SOP into a validated agentic recipe with Intake, Plan, Act, Verify.")
    audience = st.text_input("Audience / Context", value="Enterprise AV Ops team")
    outputs = st.text_input("Outputs", value="YAML recipe; short summary for KB")
with col2:
    style = st.text_input("Style / Tone", value="Direct, operational, risk-aware")
    constraints = st.text_area("Constraints", value="No secrets; verifiable steps; cite evidence sources where possible")
    variables = st.text_area("Variables (JSON, optional)", value='{"room_id": "R-123", "platform": "Zoom"}')

template = textwrap.dedent("""
{persona_block}
You are tasked to: {task}
Audience/Context: {audience}
Style/Tone: {style}
Constraints: {constraints}
Expected outputs: {outputs}
If variables are provided, use them: {variables}
Provide structured results when appropriate (JSON or YAML).
""").strip()

persona_block = ""
if choice != "(none)":
    p = persona_map[choice]
    persona_block = f"SYSTEM PERSONA:\\n{p['system_prompt']}"

preview = template.format(
    persona_block=persona_block,
    task=task, audience=audience, style=style,
    constraints=constraints, outputs=outputs, variables=variables
)

st.subheader("Preview")
st.code(preview, language="markdown")
st.download_button("Download prompt.txt", data=preview.encode("utf-8"), file_name="prompt.txt")
