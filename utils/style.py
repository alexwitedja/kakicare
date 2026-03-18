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
        '<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700'
        '&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<style>
/* ── Page background ── */
.stApp, [data-testid="stMain"], [data-testid="stAppViewContainer"] {{
    background: {BG} !important;
    font-family: 'DM Sans', sans-serif !important;
}}
section[data-testid="stSidebar"] {{
    background: {CARD} !important;
    padding: 1rem !important;
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
    padding: 2rem;
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
    font-family: 'DM Sans', sans-serif !important;
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
    font-weight: 700;
    font-size: 15px;
    padding: 14px 24px;
    box-shadow: 0 6px 18px rgba(91,168,229,0.35) !important;
    transition: opacity 0.2s;
    font-family: 'DM Sans', sans-serif !important;
}}
[data-testid="stButton"] button[kind="primary"]:hover {{
    opacity: 0.9;
}}

/* ── Secondary buttons ── */
[data-testid="stButton"] button[kind="secondary"],
button[kind="secondary"] {{
    background: {CARD} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 18px !important;
    color: {TEXT} !important;
    font-weight: 500;
    transition: border-color 0.2s;
    font-family: 'DM Sans', sans-serif !important;
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
    border: 1px solid {BORDER} !important;
    color: {NAVY} !important;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif !important;
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
    font-size: 18px !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
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
    border: 1px solid {BORDER} !important;
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
    border: 1px solid {GREEN} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: info ── */
[data-testid="stAlert"][data-type="info"] {{
    background: rgba(155,114,232,0.08) !important;
    border: 1px solid {PURPLE} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: warning ── */
[data-testid="stAlert"][data-type="warning"] {{
    background: rgba(244,162,97,0.1) !important;
    border: 1px solid {AMBER} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}
/* ── Alerts: error ── */
[data-testid="stAlert"][data-type="error"] {{
    background: rgba(214,64,69,0.08) !important;
    border: 1px solid {RED} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
}}

/* ── Bordered containers ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"][style*="border"] {{
    background: {CARD} !important;
    border-radius: 20px !important;
    border: 1px solid {BORDER} !important;
    box-shadow: 0 2px 12px rgba(91,168,229,0.08) !important;
    padding: 18px !important;
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
    border: 1px solid {BORDER} !important;
    padding: 12px 20px !important;
    font-size: 14px;
    font-family: 'DM Sans', sans-serif !important;
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
    border-radius: 12px;
    width: 52px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
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
[data-testid="stRadio"] > div > label > div:first-of-type {{
    display: none !important;
}}
[data-testid="stRadio"] > div > label > p,
[data-testid="stRadio"] > div > label > div {{
    margin: 0;
    font-size: 22px;
}}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid {BORDER} !important;
}}

/* ── Plotly charts ── */
.js-plotly-plot .plotly .bg {{
    fill: transparent !important;
}}

/* ── Global text ── */
p, span, div, label {{
    font-family: 'DM Sans', sans-serif;
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
        f'<p style="font-size:11px;font-weight:700;letter-spacing:1px;'
        f'color:{MID};text-transform:uppercase;margin:20px 0 10px 2px;'
        f'font-family:\'DM Sans\',sans-serif;">{text}</p>'
    )


def greeting_html(greeting: str, name: str, subtitle: str) -> str:
    """greeting = small context line, name = big Lora heading, subtitle = small footer."""
    greeting_part = (
        f'<p style="font-size:13px;font-weight:500;color:{MID};margin:0 0 3px 0;'
        f'font-family:\'DM Sans\',sans-serif;">{greeting}</p>'
        if greeting else ""
    )
    name_part = (
        f'<h1 style="font-family:\'Lora\',serif;font-size:27px;font-weight:600;'
        f'color:{TEXT};margin:0 0 4px 0;line-height:1.2;">{name}</h1>'
        if name else ""
    )
    subtitle_part = (
        f'<p style="font-size:12px;color:{LIGHT};margin:0 0 12px 0;'
        f'font-family:\'DM Sans\',sans-serif;">{subtitle}</p>'
        if subtitle else ""
    )
    return (
        f'<div style="margin-bottom:4px;padding:20px 0 0 0;">'
        f'{greeting_part}{name_part}{subtitle_part}'
        f'</div>'
    )


def status_banner_html(text: str, detail: str, streak: int | None = None) -> str:
    streak_badge = ""
    if streak is not None:
        streak_badge = (
            f'<div style="background:rgba(255,255,255,0.2);border-radius:14px;'
            f'padding:10px 14px;text-align:center;flex-shrink:0;">'
            f'<div style="font-size:24px;font-weight:800;color:white;">{streak}</div>'
            f'<div style="font-size:10px;color:rgba(255,255,255,0.8);">day streak</div>'
            f'</div>'
        )
    return (
        f'<div style="background:{GRAD};border-radius:22px;padding:20px 22px;'
        f'margin:12px 0 20px 0;box-shadow:0 8px 24px rgba(91,168,229,0.35);'
        f'display:flex;justify-content:space-between;align-items:center;">'
        f'<div style="flex:1;">'
        f'<p style="font-size:10px;color:rgba(255,255,255,0.75);font-weight:700;'
        f'text-transform:uppercase;letter-spacing:1.2px;margin:0 0 6px 0;'
        f'font-family:\'DM Sans\',sans-serif;">Today\'s Status</p>'
        f'<p style="color:white;font-size:20px;font-weight:700;margin:0 0 4px 0;'
        f'font-family:\'Lora\',serif;">{text}</p>'
        f'<p style="color:rgba(255,255,255,0.82);font-size:13px;margin:0;line-height:1.55;'
        f'font-family:\'DM Sans\',sans-serif;">{detail}</p>'
        f'</div>'
        f'{streak_badge}'
        f'</div>'
    )


def vital_card_html(icon: str, label: str, value: str, unit: str, status: str = "") -> str:
    dot_color = {
        "ok": GREEN,
        "warn": AMBER,
        "alert": RED,
    }.get(status, "transparent")
    dot = (
        f'<div style="width:6px;height:6px;border-radius:50%;background:{dot_color};'
        f'margin-top:8px;"></div>'
        if status else '<div style="height:14px;"></div>'
    )
    return (
        f'<div style="background:{CARD};border-radius:16px;padding:14px 12px;'
        f'box-shadow:0 2px 12px rgba(91,168,229,0.1);border:1px solid {BORDER};flex:1;">'
        f'<div style="font-size:18px;margin-bottom:4px;">{icon}</div>'
        f'<p style="font-size:10px;font-weight:600;color:{MID};text-transform:uppercase;'
        f'letter-spacing:0.5px;margin:0 0 4px 0;font-family:\'DM Sans\',sans-serif;">{label}</p>'
        f'<div style="display:flex;align-items:baseline;gap:3px;">'
        f'<span style="font-size:20px;font-weight:700;color:{TEXT};'
        f'font-family:\'DM Sans\',sans-serif;">{value}</span>'
        f'<span style="font-size:11px;font-weight:400;color:{LIGHT};'
        f'font-family:\'DM Sans\',sans-serif;">{unit}</span>'
        f'</div>'
        f'{dot}'
        f'</div>'
    )


def two_vital_row_html(card1: str, card2: str) -> str:
    return (
        f'<div style="display:flex;gap:10px;margin-bottom:10px;">'
        f'{card1}{card2}'
        f'</div>'
    )


def medication_row_html(name: str, dosage: str, time: str, taken: bool) -> str:
    if taken:
        circle = (
            f'<div style="width:22px;height:22px;border-radius:50%;background:{GREEN};'
            f'display:flex;align-items:center;justify-content:center;flex-shrink:0;">'
            f'<span style="font-size:11px;color:white;font-weight:700;">✓</span>'
            f'</div>'
        )
        name_style = f'font-size:14px;font-weight:500;color:{LIGHT};margin:0;text-decoration:line-through;'
        badge = ""
    else:
        circle = (
            f'<div style="width:22px;height:22px;border-radius:50%;background:{CARD};'
            f'border:2px solid {BORDER};flex-shrink:0;"></div>'
        )
        name_style = f'font-size:14px;font-weight:500;color:{TEXT};margin:0;'
        badge = (
            f'<span style="font-size:11px;font-weight:600;color:{AMBER};'
            f'background:#FEF3E2;padding:3px 10px;border-radius:20px;white-space:nowrap;">Due</span>'
        )
    return (
        f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;'
        f'border-bottom:1px solid {BORDER};">'
        f'{circle}'
        f'<div style="flex:1;">'
        f'<p style="{name_style}font-family:\'DM Sans\',sans-serif;">{name}</p>'
        f'<p style="margin:0;font-size:11px;color:{LIGHT};font-family:\'DM Sans\',sans-serif;">'
        f'{dosage} · {time}</p>'
        f'</div>'
        f'{badge}'
        f'</div>'
    )


def medication_card_html(rows_html: str) -> str:
    return (
        f'<div style="background:{CARD};border-radius:20px;padding:4px 18px 8px 18px;'
        f'box-shadow:0 2px 12px rgba(91,168,229,0.08);border:1px solid {BORDER};'
        f'margin-bottom:16px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:14px 0 10px 0;">'
        f'<p style="font-size:15px;font-weight:600;color:{TEXT};margin:0;'
        f'font-family:\'DM Sans\',sans-serif;">💊 Medications</p>'
        f'</div>'
        f'{rows_html}'
        f'</div>'
    )


def insight_card_html(text: str) -> str:
    return (
        f'<div style="background:linear-gradient(135deg,#EEF0FB 0%,#F0EAF8 100%);'
        f'border-radius:20px;padding:18px 20px;'
        f'border:1px solid rgba(155,114,232,0.2);margin-bottom:16px;">'
        f'<p style="font-size:10px;font-weight:700;margin:0 0 8px 0;'
        f'text-transform:uppercase;letter-spacing:1px;'
        f'background:{GRAD};-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;font-family:\'DM Sans\',sans-serif;">✨ KAKI\'s Insight</p>'
        f'<p style="font-size:13.5px;font-style:italic;color:{TEXT};margin:0 0 10px 0;'
        f'line-height:1.68;font-family:\'DM Sans\',sans-serif;">{text}</p>'
        f'<p style="font-size:11.5px;color:{MID};margin:0;'
        f'font-family:\'DM Sans\',sans-serif;">💡 Based on your last 7 days of data</p>'
        f'</div>'
    )


def chat_bubble_html(role: str, content: str) -> str:
    if role == "user":
        return (
            f'<div style="display:flex;justify-content:flex-end;margin:8px 0 14px 0;">'
            f'<div style="background:{GRAD};color:white;border-radius:18px 18px 4px 18px;'
            f'padding:12px 15px;max-width:74%;font-size:14px;line-height:1.65;'
            f'box-shadow:0 4px 14px rgba(91,168,229,0.3);'
            f'font-family:\'DM Sans\',sans-serif;">{content}</div>'
            f'</div>'
        )
    else:
        return (
            f'<div style="display:flex;align-items:flex-end;gap:8px;margin:8px 0 14px 0;">'
            f'<div style="width:30px;height:30px;border-radius:50%;background:{GRAD};'
            f'display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">💙</div>'
            f'<div style="background:{CARD};color:{TEXT};border-radius:18px 18px 18px 4px;'
            f'padding:12px 15px;max-width:74%;font-size:14px;line-height:1.65;'
            f'box-shadow:0 2px 8px rgba(0,0,0,0.07);border:1px solid {BORDER};'
            f'font-family:\'DM Sans\',sans-serif;">'
            f'{content}</div>'
            f'</div>'
        )


def suggestion_pills_html(suggestions: list[str]) -> str:
    pills = "".join(
        f'<span style="background:{CARD};border:1px solid {BORDER};border-radius:20px;'
        f'padding:7px 14px;font-size:12px;color:{NAVY};font-weight:500;white-space:nowrap;'
        f'font-family:\'DM Sans\',sans-serif;">'
        f'{s}</span>'
        for s in suggestions
    )
    return (
        f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px 0;">{pills}</div>'
    )


def crisis_banner_html(crisis_type: str) -> str:
    if crisis_type == "mental":
        title = "💙 KAKI is here with you"
        msg = (
            "You don't have to carry this alone. A real person is always available at the "
            "<strong>Samaritans of Singapore: 1-767</strong> or "
            "<strong>IMH CAREline: 6389 2222</strong> — free, confidential, 24/7."
        )
        bg = f"linear-gradient(135deg,#1E1B4B 0%,#3B1E6B 100%)"
        border = "rgba(155,114,232,0.5)"
    else:
        title = "⚠️ Contact your care team now"
        msg = (
            "Your vitals need immediate attention. "
            "<strong>Call 995 (SCDF Ambulance) immediately</strong> "
            "or go to your nearest emergency room right away."
        )
        bg = f"linear-gradient(135deg,#3D0A0A 0%,{RED} 100%)"
        border = "rgba(214,64,69,0.5)"
    return (
        f'<div style="background:{bg};border-radius:20px;padding:18px 20px;'
        f'margin:10px 0;box-shadow:0 12px 40px rgba(0,0,0,0.3);'
        f'border:1px solid {border};">'
        f'<p style="font-size:14px;font-weight:700;color:white;margin:0 0 8px 0;'
        f'font-family:\'DM Sans\',sans-serif;">🆘 {title}</p>'
        f'<p style="color:rgba(255,255,255,0.75);font-size:13px;margin:0;line-height:1.65;'
        f'font-family:\'DM Sans\',sans-serif;">{msg}</p>'
        f'</div>'
    )


def flagged_item_html(text: str) -> str:
    return (
        f'<div style="display:flex;gap:10px;padding:12px 0;'
        f'border-bottom:1px solid rgba(244,162,97,0.2);">'
        f'<span style="color:{AMBER};flex-shrink:0;font-size:14px;">•</span>'
        f'<p style="font-size:13px;color:{TEXT};margin:0;line-height:1.55;'
        f'font-family:\'DM Sans\',sans-serif;">{text}</p>'
        f'</div>'
    )


def chat_header_html() -> str:
    return (
        f'<div style="background:{GRAD};border-radius:20px;padding:14px 20px;'
        f'margin:8px 0 16px 0;'
        f'box-shadow:0 4px 20px rgba(91,168,229,0.3);">'
        f'<div style="display:flex;align-items:center;gap:12px;">'
        f'<div style="width:44px;height:44px;border-radius:50%;'
        f'background:rgba(255,255,255,0.25);'
        f'display:flex;align-items:center;justify-content:center;font-size:22px;'
        f'flex-shrink:0;border:2px solid rgba(255,255,255,0.5);">💙</div>'
        f'<div>'
        f'<p style="font-family:\'Lora\',serif;font-size:17px;font-weight:700;'
        f'color:white;margin:0;">KAKI</p>'
        f'<p style="font-size:12px;color:rgba(255,255,255,0.7);margin:0;">Your CHF Companion · Always here</p>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
