import datetime
import os

import plotly.graph_objects as go
import streamlit as st

from utils.db import (
    get_disease_profile,
    get_latest_wearables,
    get_recent_metrics,
    get_today_medications,
    get_today_metrics,
    get_user_name,
)
from utils.style import (
    greeting_html,
    insight_card_html,
    medication_card_html,
    medication_row_html,
    render_html,
    section_label_html,
    status_banner_html,
    two_vital_row_html,
    vital_card_html,
)

_TODAY = os.getenv("TODAY_OVERRIDE", "2026-03-18")


def _status(value, ok_range=None, warn_range=None) -> str:
    """Return 'ok', 'warn', or 'alert' based on value; '' if value is None."""
    if value is None:
        return ""
    if ok_range and ok_range[0] <= value <= ok_range[1]:
        return "ok"
    if warn_range and warn_range[0] <= value <= warn_range[1]:
        return "warn"
    return "alert"


def render(client, user_id: int) -> None:
    profile   = get_disease_profile(client, user_id)
    readings  = get_today_metrics(client, user_id, _TODAY)
    taken     = get_today_medications(client, user_id, _TODAY)
    history   = get_recent_metrics(client, user_id, days=7)
    wearables = get_latest_wearables(client, user_id, _TODAY)

    # --- Header ---
    name = get_user_name(client, user_id)
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 18 else "Good evening")
    render_html(greeting_html(f"{greeting}, {name} 👋", "", "March 18, 2026  ·  CHF NYHA Class II"))
    render_html(status_banner_html(
        "You're on track today",
        "Weight returning to baseline · SpO₂ stable at 96% · Keep up the good work!"
    ))

    # --- Today's Vitals ---
    render_html(section_label_html("TODAY'S VITALS"))

    def _val(key):
        return readings.get(key) if readings else None

    def _wear(key):
        return wearables.get(key) if wearables else None

    weight = _val("weight")
    sys_bp = _val("bp_systolic")
    dia_bp = _val("bp_diastolic")
    hr     = _val("heart_rate") or _wear("heart_rate")
    spo2   = _val("spo2")       or _wear("spo2")

    # Status dot logic
    weight_baseline = 74.0
    weight_status = (
        "" if weight is None
        else ("alert" if weight > weight_baseline + 2 else ("warn" if weight > weight_baseline + 1 else "ok"))
    )
    spo2_status = (
        "" if spo2 is None
        else ("alert" if spo2 < 94 else ("warn" if spo2 < 96 else "ok"))
    )
    hr_status = (
        "" if hr is None
        else ("alert" if hr > 100 else ("warn" if hr > 90 else "ok"))
    )
    bp_status = (
        "" if sys_bp is None
        else ("alert" if sys_bp > 150 else ("warn" if sys_bp > 135 else "ok"))
    )

    weight_str = f"{weight}" if weight is not None else "—"
    bp_str     = f"{sys_bp}/{dia_bp}" if sys_bp is not None and dia_bp is not None else "—"
    hr_str     = f"{hr}" if hr is not None else "—"
    spo2_str   = f"{spo2}" if spo2 is not None else "—"

    card_weight = vital_card_html("⚖️", "Weight",        weight_str, "kg",  weight_status)
    card_bp     = vital_card_html("🩺", "Blood Pressure", bp_str,     "mmHg", bp_status)
    card_hr     = vital_card_html("💓", "Heart Rate",     hr_str,     "bpm",  hr_status)
    card_spo2   = vital_card_html("🫁", "SpO₂",           spo2_str,   "%",    spo2_status)

    render_html(two_vital_row_html(card_weight, card_bp))
    render_html(two_vital_row_html(card_hr, card_spo2))

    # --- Medication Status ---
    render_html(section_label_html("MEDICATIONS"))
    if taken is None:
        st.info("No medication data logged for today.")
    else:
        rows_html = ""
        for med in profile.get("medication_schedule", []):
            med_name   = med["name"]
            dosage     = med["dosage"]
            med_taken  = taken.get(med_name, {})
            for slot in med["times"]:
                is_taken = bool(med_taken.get(slot))
                rows_html += medication_row_html(med_name, dosage, slot, is_taken)
        render_html(medication_card_html(rows_html))

    # --- AI Pattern Insight ---
    render_html(section_label_html("KAKI'S INSIGHT"))
    render_html(insight_card_html(
        "Weight has improved from 77.8 kg (Mar 16) to 75.8 kg today — returning toward baseline. "
        "SpO₂ is stable at 96%. Continue monitoring: fatigue is still present and ankle swelling was "
        "reported as recently as Mar 17. Ensure Furosemide adherence is maintained."
    ))

    # --- 7-Day BP Trend ---
    render_html(section_label_html("BLOOD PRESSURE THIS WEEK"))
    dates    = [r["date"] for r in history]
    systolic = [r.get("bp_systolic") for r in history]
    diastolic= [r.get("bp_diastolic") for r in history]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=systolic,
        fill="tozeroy",
        line=dict(color="#5BA8E5", width=2.5),
        fillcolor="rgba(91,168,229,0.12)",
        name="Systolic",
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=diastolic,
        fill="tozeroy",
        line=dict(color="#9B72E8", width=2.5),
        fillcolor="rgba(155,114,232,0.08)",
        name="Diastolic",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(font=dict(color="#6B7080", size=11)),
        xaxis=dict(showgrid=False, tickfont=dict(color="#6B7080", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#E4E6F5", tickfont=dict(color="#6B7080", size=11)),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
