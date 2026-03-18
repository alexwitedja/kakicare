from datetime import date

import streamlit as st

from utils.db import (
    get_disease_profile,
    get_today_medications,
    get_today_metrics,
    upsert_medications,
    upsert_metrics,
)
from utils.metric_config import MOOD_EMOJI_MAP, get_metric_config
from utils.style import greeting_html, render_html, section_label_html


def _render_metrics_section(metrics: list[str], existing_readings: dict) -> dict:
    """Render number inputs for each tracked metric. Returns {metric_name: value}."""
    values = {}
    rendered_groups: set[str] = set()
    i = 0
    while i < len(metrics):
        metric = metrics[i]
        cfg = get_metric_config(metric)
        group = cfg.get("group")

        if group and group not in rendered_groups:
            group_metrics = [m for m in metrics if get_metric_config(m).get("group") == group]
            rendered_groups.add(group)
            cols = st.columns(len(group_metrics))
            for col, gm in zip(cols, group_metrics):
                gcfg = get_metric_config(gm)
                label = f"{gcfg['label']} ({gcfg['unit']})" if gcfg["unit"] else gcfg["label"]
                default_val = existing_readings.get(gm, gcfg["default"])
                with col:
                    if gcfg["type"] == "int":
                        values[gm] = st.number_input(
                            label,
                            min_value=int(gcfg["min"]),
                            max_value=int(gcfg["max"]),
                            value=int(default_val),
                            step=int(gcfg["step"]),
                            key=f"metric_{gm}",
                        )
                    else:
                        values[gm] = st.number_input(
                            label,
                            min_value=float(gcfg["min"]),
                            max_value=float(gcfg["max"]),
                            value=float(default_val),
                            step=float(gcfg["step"]),
                            key=f"metric_{gm}",
                            format="%.1f",
                        )
        elif not group:
            label = f"{cfg['label']} ({cfg['unit']})" if cfg["unit"] else cfg["label"]
            default_val = existing_readings.get(metric, cfg["default"])
            if cfg["type"] == "int":
                values[metric] = st.number_input(
                    label,
                    min_value=int(cfg["min"]),
                    max_value=int(cfg["max"]),
                    value=int(default_val),
                    step=int(cfg["step"]),
                    key=f"metric_{metric}",
                )
            else:
                values[metric] = st.number_input(
                    label,
                    min_value=float(cfg["min"]),
                    max_value=float(cfg["max"]),
                    value=float(default_val),
                    step=float(cfg["step"]),
                    key=f"metric_{metric}",
                    format="%.1f",
                )
        i += 1

    return values


def _render_mood_section(mood_options: list[str], existing_mood: str | None) -> str:
    """Render mood radio. Returns raw key e.g. 'bad'."""
    emoji_labels = [MOOD_EMOJI_MAP.get(m, m) for m in mood_options]
    reverse_map = {v: k for k, v in MOOD_EMOJI_MAP.items()}

    default_index = 0
    if existing_mood and existing_mood in mood_options:
        default_index = mood_options.index(existing_mood)

    st.write("**How are you feeling today?**")
    selected_label = st.radio(
        "Mood",
        options=emoji_labels,
        index=default_index,
        horizontal=True,
        label_visibility="collapsed",
        key="mood_radio",
    )
    return reverse_map.get(selected_label, mood_options[0])


def _render_symptoms_section(
    symptom_options: list[str], existing_symptoms: list[str]
) -> list[str]:
    """Render symptom multiselect + free-text. Returns merged list."""
    preset_defaults = [s for s in existing_symptoms if s in symptom_options]
    custom_existing = [s for s in existing_symptoms if s not in symptom_options]
    custom_text = ", ".join(custom_existing)

    st.write("**Symptoms today** (select all that apply)")
    selected_presets = st.multiselect(
        "Symptoms",
        options=symptom_options,
        default=preset_defaults,
        format_func=lambda s: s.replace("_", " ").title(),
        label_visibility="collapsed",
        key="symptoms_multiselect",
    )

    custom_input = st.text_input(
        "Other symptoms (comma-separated)",
        value=custom_text,
        placeholder="e.g. headache, nausea",
        key="symptoms_custom",
    )

    custom_list = [s.strip() for s in custom_input.split(",") if s.strip()]
    return selected_presets + custom_list


def _render_medications_section(
    medications: list[dict], existing_taken: dict
) -> dict:
    """Render checkbox grid for medication adherence. Returns {med_name: {time: bool}}."""
    taken = {}
    for med in medications:
        name = med.get("name", "Unknown")
        dosage = med.get("dosage", "")
        times = med.get("times", [])
        label = f"**{name}** — {dosage}" if dosage else f"**{name}**"
        st.write(label)
        if not times:
            st.caption("No scheduled times.")
            taken[name] = {}
            continue
        cols = st.columns(len(times))
        time_taken = {}
        for col, time_slot in zip(cols, times):
            default_checked = existing_taken.get(name, {}).get(time_slot, False)
            with col:
                time_taken[time_slot] = st.checkbox(
                    time_slot,
                    value=default_checked,
                    key=f"med_{name}_{time_slot}",
                )
        taken[name] = time_taken
    return taken


def render(client, user_id: int) -> None:
    today = date.today().isoformat()

    render_html(greeting_html("Log your health data", "Today's Log", today))

    try:
        profile = get_disease_profile(client, user_id)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

    metrics_list: list[str] = profile.get("tracked_metrics", [])
    mood_options: list[str] = profile.get("mood_options", list(MOOD_EMOJI_MAP.keys()))
    symptom_options: list[str] = profile.get("symptom_options", [])
    medications: list[dict] = profile.get("medication_schedule", [])

    existing_readings: dict = {}
    existing_taken: dict = {}
    try:
        today_metrics = get_today_metrics(client, user_id, today)
        if today_metrics:
            existing_readings = today_metrics
    except RuntimeError as e:
        st.warning(f"Could not load today's metrics: {e}")

    try:
        today_meds = get_today_medications(client, user_id, today)
        if today_meds:
            existing_taken = today_meds
    except RuntimeError as e:
        st.warning(f"Could not load today's medications: {e}")

    existing_mood: str | None = existing_readings.get("mood")
    existing_symptoms: list[str] = existing_readings.get("symptoms", [])

    with st.form("track_form"):
        render_html(section_label_html("VITALS"))
        metric_values = _render_metrics_section(metrics_list, existing_readings)

        st.divider()
        render_html(section_label_html("MOOD & SYMPTOMS"))
        mood_value = _render_mood_section(mood_options, existing_mood)
        symptoms_value = _render_symptoms_section(symptom_options, existing_symptoms)

        st.divider()
        render_html(section_label_html("MEDICATIONS"))
        if medications:
            taken_value = _render_medications_section(medications, existing_taken)
        else:
            st.info("No medications found in your profile.")
            taken_value = {}

        submitted = st.form_submit_button("Save Today's Log", type="primary")

    if submitted:
        readings = {**metric_values, "mood": mood_value, "symptoms": symptoms_value}
        errors = []
        try:
            upsert_metrics(client, user_id, today, readings)
        except RuntimeError as e:
            errors.append(str(e))
        try:
            upsert_medications(client, user_id, today, taken_value)
        except RuntimeError as e:
            errors.append(str(e))

        if errors:
            for err in errors:
                st.error(err)
        else:
            st.success("Health log saved successfully!")
