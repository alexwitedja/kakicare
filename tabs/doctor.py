import plotly.graph_objects as go
import streamlit as st

from utils.db import get_recent_metrics
from utils.style import (
    flagged_item_html,
    greeting_html,
    render_html,
    section_label_html,
)

SOAP_SUMMARY = """
### Subjective
Patient Marcus Chen (67, CHF NYHA Class II) reported progressive symptoms over the monitoring period (Mar 2–18, 2026):
- **Fatigue** — onset Mar 8, worsening through Mar 16
- **Ankle swelling** — onset Mar 14, bilateral
- **Shortness of breath** — onset Mar 15, on exertion
- **Difficulty lying flat** — reported Mar 16 (possible orthopnea)
- Patient expressed concern about rapid weight gain on Mar 16

### Objective
| Metric | Mar 10 | Mar 16 | Change |
|---|---|---|---|
| Weight | 75.5 kg | 77.8 kg | **+2.3 kg** |
| BP | 131/80 mmHg | 145/90 mmHg | Trending up |
| Resting HR | ~70 bpm | 96 bpm | Elevated |
| SpO₂ | 96% | 91% | **Below threshold** |
| Steps/day | ~4,200 | 1,200 | Markedly reduced |

Wearable data (Mar 15–16): HR elevated 88–96 bpm, SpO₂ dipped to 91% on Mar 16.

Medication adherence: Two missed PM Furosemide doses — Mar 13 (20:00) and Mar 14 (14:00 & 20:00).

### Assessment
Pattern consistent with **early CHF decompensation**:
- Weight threshold breached (>2 kg gain in 2 days) on Mar 15–16
- SpO₂ below 94% threshold on Mar 15–16
- Symptom cluster (dyspnea, orthopnea, ankle oedema, fatigue) aligns with fluid overload
- Medication non-adherence (Furosemide) likely contributed to decompensation trajectory

### Plan
1. Review diuretic adherence and address barriers to medication compliance
2. Assess current fluid status (weight trend, oedema, JVP if available)
3. Consider Furosemide dose adjustment if weight has not normalised
4. Follow up wearable HR/SpO₂ trends closely over next 48–72 hours
5. Consider early clinic review given SpO₂ dip and orthopnea symptom
"""

FLAGGED_ITEMS = [
    "Weight gain +2.3 kg over 6 days (Mar 10–16) — threshold breached (>2 kg / 2 days)",
    "SpO₂ dropped to 91% on Mar 16 (below 94% threshold)",
    "Missed Furosemide PM doses: Mar 13 (20:00), Mar 14 (14:00 & 20:00)",
    "Resting HR peaked at 96 bpm on Mar 16 (elevated above baseline ~70 bpm)",
    "Reported difficulty lying flat — possible orthopnea (Mar 16)",
]


def _plotly_area(x, traces: list[dict]) -> go.Figure:
    """Build a transparent-background area chart from trace dicts."""
    fig = go.Figure()
    for t in traces:
        fig.add_trace(go.Scatter(
            x=x,
            y=t["y"],
            fill="tozeroy",
            line=dict(color=t["color"], width=2.5),
            fillcolor=t["fill"],
            name=t["name"],
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
    return fig


def render(client, user_id: int) -> None:
    render_html(greeting_html(
        "For your next visit",
        "Doctor Summary",
        "Patient: Marcus Chen, 67  ·  CHF NYHA Class II"
    ))

    with st.container(border=True):
        st.markdown(SOAP_SUMMARY)

    render_html(section_label_html("FLAGGED FOR DISCUSSION"))
    items_html = "".join(flagged_item_html(item) for item in FLAGGED_ITEMS)
    render_html(
        f'<div style="background:#FFFBEC;border-radius:20px;padding:6px 18px 6px 18px;'
        f'border:1px solid rgba(244,162,97,0.3);margin-bottom:16px;">'
        f'<p style="font-size:12px;font-weight:700;color:#F4A261;margin:14px 0 10px 0;'
        f'text-transform:uppercase;letter-spacing:0.8px;">⚠️ Flagged for Discussion</p>'
        f'{items_html}'
        f'</div>'
    )

    history = get_recent_metrics(client, user_id, days=14)
    dates = [r["date"] for r in history]

    render_html(section_label_html("WEIGHT TREND (14 DAYS)"))
    weight_vals = [r.get("weight") for r in history]
    fig_weight = _plotly_area(dates, [
        {"y": weight_vals, "color": "#5BA8E5", "fill": "rgba(91,168,229,0.12)", "name": "Weight (kg)"},
    ])
    st.plotly_chart(fig_weight, use_container_width=True, config={"displayModeBar": False})

    render_html(section_label_html("BLOOD PRESSURE TREND (14 DAYS)"))
    systolic  = [r.get("bp_systolic")  for r in history]
    diastolic = [r.get("bp_diastolic") for r in history]
    fig_bp = _plotly_area(dates, [
        {"y": systolic,  "color": "#5BA8E5", "fill": "rgba(91,168,229,0.12)", "name": "Systolic"},
        {"y": diastolic, "color": "#9B72E8", "fill": "rgba(155,114,232,0.08)", "name": "Diastolic"},
    ])
    st.plotly_chart(fig_bp, use_container_width=True, config={"displayModeBar": False})

    st.button("Share with Doctor", type="primary", icon="📤")
    # TODO: implement share/export via n8n Export workflow
