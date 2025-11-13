
# 12_Chat_Persona.py
import streamlit as st
from core.ipav_shared import list_agent_personas, call_llm

st.set_page_config(page_title="Persona Chat", page_icon="💬")
st.title("💬 Persona Chat")

personas = list_agent_personas()
persona_map = {p["name"]: p for p in personas}
persona_name = st.selectbox("Persona", list(persona_map.keys()) or ["(no personas yet)"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if personas:
    system_prompt = persona_map[persona_name]["system_prompt"]
else:
    system_prompt = "You are a helpful assistant for Agentic AV Ops."

for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Ask something…")
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Model call
    response = call_llm(user_input, system=system_prompt)
    st.session_state.chat_history.append(("assistant", response))

    with st.chat_message("assistant"):
        st.markdown(response)

with st.sidebar:
    if st.button("Reset conversation"):
        st.session_state.chat_history = []
        st.experimental_rerun()
