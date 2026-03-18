import streamlit as st

from utils.style import (
    chat_bubble_html,
    chat_header_html,
    crisis_banner_html,
    render_html,
    section_label_html,
)

_QUICK_SUGGESTIONS = [
    "How am I doing this week?",
    "Run a health check for me",
    "I'm feeling more tired than usual",
    "Did I miss any medications?",
]

_MENTAL_CRISIS = [
    "suicide", "kill myself", "end my life", "don't want to live",
    "want to die", "harm myself", "self-harm", "no point living",
]
_VITALS_CRISIS = [
    "chest pain", "chest tightness", "can't breathe", "cannot breathe",
    "difficulty breathing", "trouble breathing", "i collapsed", "i fainted",
    "heart attack", "stroke", "unconscious",
]


def _detect_crisis(text: str) -> str | None:
    lower = text.lower()
    if any(k in lower for k in _MENTAL_CRISIS):
        return "mental"
    if any(k in lower for k in _VITALS_CRISIS):
        return "vitals"
    return None


def _get_response(prompt: str) -> str:
    # TODO: replace with n8n chatbot webhook call
    return "_KAKI is not connected yet — n8n integration coming soon._"


def render(user_id: int) -> None:
    if "kaki_messages" not in st.session_state:
        st.session_state.kaki_messages = []

    render_html(chat_header_html())

    if st.session_state.kaki_messages:
        if st.button("Clear chat", key="clear_chat"):
            st.session_state.kaki_messages = []
            st.rerun()

    # Render message history
    for msg in st.session_state.kaki_messages:
        render_html(chat_bubble_html(msg["role"], msg["content"]))
        if msg.get("crisis"):
            render_html(crisis_banner_html(msg["crisis"]))

    # Quick suggestions (only when chat is empty)
    if not st.session_state.kaki_messages:
        render_html(section_label_html("What would you like to talk about?"))
        cols = st.columns(2)
        for i, suggestion in enumerate(_QUICK_SUGGESTIONS):
            with cols[i % 2]:
                if st.button(suggestion, key=f"qs_{i}", use_container_width=True):
                    st.session_state.kaki_pending = suggestion
                    st.rerun()

    prompt: str | None = st.chat_input("Message KAKI...")
    if "kaki_pending" in st.session_state:
        prompt = st.session_state.pop("kaki_pending")

    if prompt:
        crisis = _detect_crisis(prompt)
        st.session_state.kaki_messages.append({"role": "user", "content": prompt, "crisis": None})
        response = _get_response(prompt)
        st.session_state.kaki_messages.append({"role": "assistant", "content": response, "crisis": crisis})
        st.rerun()
