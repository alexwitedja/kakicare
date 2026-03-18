# Design tokens
BG      = "#F2F3FA"
CARD    = "#FFFFFF"
TEXT    = "#1E1B4B"
MID     = "#6B7080"
LIGHT   = "#A8B4CC"
BORDER  = "#E4E6F5"
BLUE    = "#5BA8E5"
PURPLE  = "#9B72E8"
NAVY    = "#3B3DAA"
GREEN   = "#52B788"
AMBER   = "#F4A261"
CORAL   = "#E07B8A"
RED     = "#D64045"
GRAD    = "linear-gradient(135deg, #5BA8E5 0%, #9B72E8 100%)"

import streamlit as st


def inject_css() -> None:
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<style>
/* ── Page background ── */
.stApp, [data-testid="stMain"], [data-testid="stAppViewContainer"] {{
    background: {BG} !important;
}}
section[data-testid="stSidebar"] {{
    background: {CARD} !important;
}}
[data-testid="stHeader"] {{
    background: transparent !important;
}}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{
    display: none !important;
}}

/* ── Tab bar ── */
[data-testid="stTabs"] > div:first-child {{
    background: {CARD};
    border-radius: 14px;
    padding: 4px;
    gap: 2px;
    box-shadow: 0 2px 12px rgba(91,168,229,0.08);
}}
[data-testid="stTabs"] button[data-baseweb="tab"] {{
    border-radius: 10px !important;
    color: {MID} !important;
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    border: none !important;
    background: transparent !important;
    transition: all 0.2s;
}}
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {{
    background: {GRAD} !important;
    color: white !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    display: none !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-border"] {{
    display: none !important;
}}

/* ── Primary buttons ── */
[data-testid="stButton"] button[kind="primary"],
button[kind="primary"] {{
    background: {GRAD} !important;
    border: none !important;
    border-radius: 18px !important;
    color: white !important;
    font-weight: 600;
    padding: 10px 24px;
    box-shadow: 0 4px 14px rgba(91,168,229,0.3) !important;
    transition: opacity 0.2s;
}}
[data-testid="stButton"] button[kind="primary"]:hover {{
    opacity: 0.9;
}}

/* ── Secondary buttons ── */
[data-testid="stButton"] button[kind="secondary"],
button[kind="secondary"] {{
    background: {CARD} !important;
    border: 1.5px solid {BORDER} !important;
    border-radius: 18px !important;
    color: {TEXT} !important;
    font-weight: 500;
    transition: border-color 0.2s;
}}
[data-testid="stButton"] button[kind="secondary"]:hover {{
    border-color: {BLUE} !important;
}}

/* ── Suggestion pill buttons ── */
div[data-testid="stHorizontalBlock"] [data-testid="stButton"] button {{
    border-radius: 20px !important;
    font-size: 12px !important;
    white-space: nowrap !important;
    padding: 7px 13px !important;
    background: {CARD} !important;
    border: 1.5px solid {BORDER} !important;
    color: {TEXT} !important;
    font-weight: 500;
}}
div[data-testid="stHorizontalBlock"] [data-testid="stButton"] button:hover {{
    border-color: {BLUE} !important;
    background: rgba(91,168,229,0.06) !important;
}}

/* ── Number/text inputs ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {{
    background: {BG} !important;
    border-radius: 12px !important;
    border: 2px solid transparent !important;
    color: {TEXT} !important;
    transition: border-color 0.2s;
}}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {{
    border-color: {BLUE} !important;
    box-shadow: 0 0 0 2px rgba(91,168,229,0.15) !important;
}}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] > div > div {{
    background: {BG} !important;
    border-radius: 12px !important;
    border: 2px solid {BORDER} !important;
}}

/* ── Checkboxes ── */
[data-testid="stCheckbox"] label span {{
    background-color: {BG} !important;
    border-color: {BORDER} !important;
    border-radius: 6px !important;
}}

/* ── Alerts: success ── */
[data-testid="stAlert"][data-type="success"] {{
    background: rgba(82,183,136,0.1) !important;
    border: 1.5px solid {GREEN} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: info ── */
[data-testid="stAlert"][data-type="info"] {{
    background: rgba(155,114,232,0.08) !important;
    border: 1.5px solid {PURPLE} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: warning ── */
[data-testid="stAlert"][data-type="warning"] {{
    background: rgba(244,162,97,0.1) !important;
    border: 1.5px solid {AMBER} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: error ── */
[data-testid="stAlert"][data-type="error"] {{
    background: rgba(214,64,69,0.08) !important;
    border: 1.5px solid {RED} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}

/* ── Bordered containers ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"][style*="border"] {{
    background: {CARD} !important;
    border-radius: 16px !important;
    border: 1.5px solid {BORDER} !important;
    box-shadow: 0 2px 12px rgba(91,168,229,0.08) !important;
    padding: 16px !important;
}}

/* ── Divider ── */
hr {{
    border-color: {BORDER} !important;
    opacity: 1 !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
    border-radius: 24px !important;
    background: {BG} !important;
    border: 2px solid {BORDER} !important;
    padding: 12px 20px !important;
    font-size: 14px;
    transition: border-color 0.2s;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {BLUE} !important;
    box-shadow: 0 0 0 2px rgba(91,168,229,0.15) !important;
}}

/* ── Chat message bubbles ── */
[data-testid="stChatMessage"] {{
    background: transparent !important;
    padding: 0 !important;
}}

/* ── Radio buttons (mood) ── */
[data-testid="stRadio"] > div > label {{
    background: {BG};
    border: 2px solid {BORDER};
    border-radius: 50%;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    margin: 4px;
}}
[data-testid="stRadio"] > div > label:has(input:checked) {{
    border-color: {PURPLE} !important;
    background: rgba(155,114,232,0.1) !important;
}}
[data-testid="stRadio"] [data-testid="stWidgetLabel"] {{
    display: none;
}}
[data-testid="stRadio"] > div {{
    display: flex;
    flex-direction: row;
    gap: 8px;
    flex-wrap: wrap;
}}
[data-testid="stRadio"] > div input[type="radio"] {{
    display: none;
}}
/* Hide the text span inside radio label, show only emoji */
[data-testid="stRadio"] > div > label > div {{
    display: none;
}}
[data-testid="stRadio"] > div > label > p {{
    margin: 0;
}}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden;
    border: 1.5px solid {BORDER} !important;
}}

/* ── Plotly charts ── */
.js-plotly-plot .plotly .bg {{
    fill: transparent !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )


def render_html(html: str) -> None:
    st.markdown(html, unsafe_allow_html=True)


# ── HTML helpers ─────────────────────────────────────────────────────────────

def section_label_html(text: str) -> str:
    return (
        f'<p style="font-size:11px;font-weight:700;letter-spacing:0.08em;'
        f'color:{MID};text-transform:uppercase;margin:20px 0 8px 2px;">{text}</p>'
    )


def greeting_html(greeting: str, name: str, subtitle: str) -> str:
    name_part = (
        f'<span style="font-family:\'Lora\',serif;font-size:28px;font-weight:700;'
        f'color:{TEXT};">{name}</span>'
        if name else ""
    )
    greeting_part = (
        f'<p style="font-family:\'Lora\',serif;font-size:24px;font-weight:600;'
        f'color:{TEXT};margin:0 0 2px 0;">{greeting}</p>'
    )
    subtitle_part = (
        f'<p style="font-size:13px;color:{MID};margin:2px 0 12px 0;">{subtitle}</p>'
        if subtitle else ""
    )
    return (
        f'<div style="margin-bottom:4px;">'
        f'{greeting_part}{name_part}{subtitle_part}'
        f'</div>'
    )


def status_banner_html(text: str, detail: str) -> str:
    return (
        f'<div style="background:{GRAD};border-radius:22px;padding:20px 24px;'
        f'margin:12px 0 20px 0;box-shadow:0 6px 24px rgba(91,168,229,0.28);">'
        f'<p style="color:white;font-size:16px;font-weight:700;margin:0 0 4px 0;">{text}</p>'
        f'<p style="color:rgba(255,255,255,0.82);font-size:13px;margin:0;">{detail}</p>'
        f'</div>'
    )


def vital_card_html(icon: str, label: str, value: str, unit: str, status: str = "") -> str:
    dot_color = {
        "ok": GREEN,
        "warn": AMBER,
        "alert": RED,
    }.get(status, "transparent")
    dot = (
        f'<span style="width:8px;height:8px;border-radius:50%;background:{dot_color};'
        f'display:inline-block;margin-left:6px;vertical-align:middle;"></span>'
        if status else ""
    )
    return (
        f'<div style="background:{CARD};border-radius:16px;padding:16px 18px;'
        f'box-shadow:0 2px 12px rgba(91,168,229,0.08);border:1.5px solid {BORDER};flex:1;">'
        f'<div style="font-size:22px;margin-bottom:4px;">{icon}</div>'
        f'<p style="font-size:11px;font-weight:600;color:{MID};text-transform:uppercase;'
        f'letter-spacing:0.06em;margin:0 0 4px 0;">{label}</p>'
        f'<p style="font-size:22px;font-weight:700;color:{TEXT};margin:0;line-height:1.1;">'
        f'{value}<span style="font-size:13px;font-weight:400;color:{MID};margin-left:4px;">'
        f'{unit}</span>{dot}</p>'
        f'</div>'
    )


def two_vital_row_html(card1: str, card2: str) -> str:
    return (
        f'<div style="display:flex;gap:12px;margin-bottom:12px;">'
        f'{card1}{card2}'
        f'</div>'
    )


def medication_row_html(name: str, dosage: str, time: str, taken: bool) -> str:
    circle_style = (
        f'width:22px;height:22px;border-radius:50%;display:inline-flex;'
        f'align-items:center;justify-content:center;font-size:13px;flex-shrink:0;'
        f'background:{"rgba(82,183,136,0.15)" if taken else "rgba(214,64,69,0.08)"};'
        f'border:2px solid {GREEN if taken else RED};'
    )
    icon = "✓" if taken else "✗"
    icon_color = GREEN if taken else RED
    return (
        f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;'
        f'border-bottom:1px solid {BORDER};">'
        f'<div style="{circle_style}"><span style="color:{icon_color};font-weight:700;">{icon}</span></div>'
        f'<div style="flex:1;">'
        f'<p style="margin:0;font-size:14px;font-weight:600;color:{TEXT};">{name}</p>'
        f'<p style="margin:0;font-size:12px;color:{MID};">{dosage} · {time}</p>'
        f'</div>'
        f'</div>'
    )


def medication_card_html(rows_html: str) -> str:
    return (
        f'<div style="background:{CARD};border-radius:16px;padding:4px 18px 8px 18px;'
        f'box-shadow:0 2px 12px rgba(91,168,229,0.08);border:1.5px solid {BORDER};'
        f'margin-bottom:16px;">'
        f'{rows_html}'
        f'</div>'
    )


def insight_card_html(text: str) -> str:
    return (
        f'<div style="background:linear-gradient(135deg,rgba(91,168,229,0.08) 0%,'
        f'rgba(155,114,232,0.10) 100%);border-radius:16px;padding:18px 20px;'
        f'border:1.5px solid {BORDER};margin-bottom:16px;">'
        f'<p style="font-size:13px;font-style:italic;color:{TEXT};margin:0;line-height:1.65;">'
        f'📊 {text}</p>'
        f'</div>'
    )


def chat_bubble_html(role: str, content: str) -> str:
    if role == "user":
        return (
            f'<div style="display:flex;justify-content:flex-end;margin:8px 0;">'
            f'<div style="background:{GRAD};color:white;border-radius:18px 18px 4px 18px;'
            f'padding:11px 16px;max-width:78%;font-size:14px;line-height:1.55;'
            f'box-shadow:0 2px 8px rgba(91,168,229,0.2);">{content}</div>'
            f'</div>'
        )
    else:
        return (
            f'<div style="display:flex;align-items:flex-start;gap:10px;margin:8px 0;">'
            f'<div style="width:32px;height:32px;border-radius:50%;background:{GRAD};'
            f'display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">💙</div>'
            f'<div style="background:{CARD};color:{TEXT};border-radius:18px 18px 18px 4px;'
            f'padding:11px 16px;max-width:78%;font-size:14px;line-height:1.55;'
            f'box-shadow:0 2px 8px rgba(91,168,229,0.08);border:1.5px solid {BORDER};">'
            f'{content}</div>'
            f'</div>'
        )


def suggestion_pills_html(suggestions: list[str]) -> str:
    pills = "".join(
        f'<span style="background:{CARD};border:1.5px solid {BORDER};border-radius:20px;'
        f'padding:7px 14px;font-size:12px;color:{TEXT};font-weight:500;white-space:nowrap;">'
        f'{s}</span>'
        for s in suggestions
    )
    return (
        f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px 0;">{pills}</div>'
    )


def crisis_banner_html(crisis_type: str) -> str:
    if crisis_type == "mental":
        msg = (
            "It sounds like you may be in emotional distress. "
            "Please reach out to the <strong>Samaritans of Singapore: 1-767</strong> (24/7) "
            "or text <strong>IMH CAREline: 6389 2222</strong>. You are not alone. 💙"
        )
        bg = f"linear-gradient(135deg,{NAVY} 0%,#5B3DAA 100%)"
    else:
        msg = (
            "This sounds like a medical emergency. "
            "<strong>Call 995 (SCDF Ambulance) immediately</strong> or ask someone nearby for help."
        )
        bg = f"linear-gradient(135deg,{RED} 0%,#A01B1B 100%)"
    return (
        f'<div style="background:{bg};border-radius:14px;padding:16px 20px;'
        f'margin:10px 0;box-shadow:0 4px 16px rgba(0,0,0,0.25);">'
        f'<p style="color:white;font-size:14px;margin:0;line-height:1.6;">🆘 {msg}</p>'
        f'</div>'
    )


def flagged_item_html(text: str) -> str:
    return (
        f'<div style="background:#FFFBEC;border-left:4px solid {AMBER};border-radius:0 10px 10px 0;'
        f'padding:12px 16px;margin:8px 0;font-size:13px;color:{TEXT};line-height:1.55;">'
        f'⚠️ {text}'
        f'</div>'
    )


def chat_header_html() -> str:
    return (
        f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">'
        f'<div style="width:48px;height:48px;border-radius:50%;background:{GRAD};'
        f'display:flex;align-items:center;justify-content:center;font-size:24px;'
        f'box-shadow:0 4px 14px rgba(91,168,229,0.3);">💙</div>'
        f'<div>'
        f'<p style="font-family:\'Lora\',serif;font-size:22px;font-weight:700;color:{TEXT};margin:0;">KAKI</p>'
        f'<p style="font-size:13px;color:{MID};margin:0;">Your AI health companion</p>'
        f'</div>'
        f'</div>'
    )
