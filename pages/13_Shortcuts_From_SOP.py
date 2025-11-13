
# 13_Shortcuts_From_SOP.py
import json, re, io, yaml
import streamlit as st
from core.ipav_shared import save_shortcut

st.set_page_config(page_title="Generate Shortcut from SOP", page_icon="⚡")
st.title("⚡ Generate Shortcut from SOP (Small Flows)")

st.markdown("Paste an SOP and produce a reusable Shortcut object and an optional Recipe YAML.")

col1, col2 = st.columns(2)
with col1:
    label = st.text_input("Label*", value="Executive report with sections")
    description = st.text_area("Description", value="Generate an executive report in sections based on provided inputs.")
    fmt = st.selectbox("Format", ["MD", "json", "yaml"])
with col2:
    verbosity = st.selectbox("Verbosity", ["low", "medium", "high"], index=1)
    reasoning = st.selectbox("Reasoning", ["low", "medium", "high"], index=1)
    instructions = st.text_area("Instructions", value="Use clear headings")

sop_text = st.text_area("SOP Text", height=220, value="""Steps:
1) Gather inputs
2) Plan actions
3) Execute tasks
4) Verify outputs
""")

# Parse SOP into a dict of key:value slots (best-effort)
def parse_sop_to_template(s: str):
    lines = [ln.strip("-• ").strip() for ln in s.splitlines() if ln.strip()]
    steps = []
    for ln in lines:
        m = re.match(r"^\d+[\).\s-]*(.*)", ln)
        step = m.group(1).strip() if m else ln
        if step.lower().startswith(("step", "steps")):
            continue
        steps.append(step)
    tmpl = {"steps": steps or ["Gather inputs", "Plan", "Act", "Verify"]}
    return tmpl

if st.button("Generate Shortcut"):
    template = parse_sop_to_template(sop_text)
    shortcut = {
        "Label": label,
        "Description": description,
        "Template": template,
        "Instructions": instructions,
        "Format": fmt,
        "Verbosity": verbosity,
        "Reasoning": reasoning
    }
    st.subheader("Shortcut JSON")
    st.code(json.dumps(shortcut, indent=2, ensure_ascii=False), language="json")

    # Save to DB
    sid = save_shortcut(shortcut)
    st.success(f"Saved shortcut (id: {sid[:8]}…).")

    # Minimal recipe YAML from SOP
    recipe_yaml = {
        "name": f"Recipe — {label}",
        "description": description or "Generated from SOP",
        "intake": [{"gather": "inputs"}],
        "plan": [{"step": "Plan actions based on inputs"}],
        "act": [{"action": "Execute tasks from SOP"}],
        "verify": [{"check": "Validate outputs and summarize"}]
    }
    st.subheader("Recipe YAML (starter)")
    st.code(yaml.safe_dump(recipe_yaml, sort_keys=False), language="yaml")

    # Download buttons
    st.download_button("Download shortcut.json", data=json.dumps(shortcut, indent=2).encode("utf-8"),
                       file_name="shortcut.json")
    st.download_button("Download recipe.yaml", data=yaml.safe_dump(recipe_yaml, sort_keys=False).encode("utf-8"),
                       file_name="recipe.yaml")
else:
    st.info("Fill fields and click **Generate Shortcut** to produce JSON and YAML.")
