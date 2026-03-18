# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**KAKI Care** — a companion app for chronic disease patients (demo: CHF/Congestive Heart Failure) for the NUS-Synapxe-IMDA AI Innovation Challenge 2026. Core goal: detect decompensation before crisis via passive monitoring, smart alerts, and doctor-ready SOAP summaries.

**Status:** Active development. Database schema and mock data are finalized; Streamlit frontend is built; n8n workflows are still being integrated (chatbot backend is a stub).

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (SQLite backend, no external services needed)
streamlit run app.py
```

There are no tests or linting configs in this repo. The SQLite path (`kaki_care.db`) is auto-created on first run and can be deleted to reset demo data.

Copy `.env.example` to `.env` before running. Key env vars:

| Variable | Default | Purpose |
|---|---|---|
| `DB_BACKEND` | `sqlite` | `sqlite` (local) or `supabase` (production) |
| `SQLITE_PATH` | `kaki_care.db` | SQLite file path |
| `SUPABASE_URL` / `SUPABASE_KEY` | — | Required when `DB_BACKEND=supabase` |
| `USER_ID` | `1` | Patient user ID |
| `TODAY_OVERRIDE` | `2026-03-18` | Override "today" date for demo (used in `tabs/home.py`) |

## Architecture

### Dual-Backend DB Layer

`utils/db.py` is the **only public interface** for data access. It routes every call to either `utils/sqlite_db.py` or `utils/supabase_db.py` based on `DB_BACKEND`. Callers never import from the backend modules directly.

`sqlite_db.py` auto-creates the schema and seeds Marcus Chen's demo data on first connection (`@st.cache_resource`). The SQLite schema mirrors the Supabase schema — JSONB columns become `TEXT` storing JSON strings.

`disease_profile` data from both backends goes through `_normalize_profile()` in `db.py`, which flattens the nested `{"diseases": [...], "medications": [...]}` structure into a flat dict with `tracked_metrics`, `symptom_options`, `mood_options`, `medication_schedule`.

### Streamlit App Structure

`app.py` creates a single-page 4-tab layout. Each tab is a module in `tabs/` with a `render(client, user_id)` function (chat tab takes only `user_id`).

- **`tabs/home.py`** — reads vitals/wearables/meds, renders metric cards, a hardcoded AI insight string, and a 7-day BP line chart
- **`tabs/chat.py`** — chat UI with keyword-based crisis detection (`_detect_crisis()`). On crisis, a banner is injected into the assistant message turn (does not block the chat flow). `_get_response()` is a **stub** pending n8n webhook integration. Chat history lives in `st.session_state.kaki_messages`; suggestion pills use `st.session_state.kaki_pending` as a one-shot trigger.
- **`tabs/track.py`** — form-based daily logging; reads profile to render only the patient's tracked metrics dynamically; upserts on submit
- **`tabs/doctor.py`** — renders a **hardcoded** SOAP summary and flagged items (static strings), plus live 14-day trend charts from DB. "Share with Doctor" button is a stub pending n8n Export workflow.

### UI / Design System

All visual output goes through `utils/style.py`. Never use `st.markdown` directly for styled content in tabs — use the helpers:

- **`render_html(html)`** — thin wrapper around `st.markdown(..., unsafe_allow_html=True)`
- **HTML builder functions** — `vital_card_html`, `medication_row_html`, `chat_bubble_html`, `crisis_banner_html`, `flagged_item_html`, `greeting_html`, `status_banner_html`, etc.
- **Design tokens** — color constants (`BG`, `CARD`, `TEXT`, `BLUE`, `PURPLE`, `GREEN`, `AMBER`, `RED`, `GRAD`, etc.) are defined at the top of `style.py` and used inside every HTML builder. Import them directly when building new HTML strings.
- `inject_css()` is called once in `app.py` at startup; it loads Lora font and overrides Streamlit's default chrome via `!important` rules.

### Metric Configuration

`utils/metric_config.py` defines display config (label, unit, type, min/max/step/default) for known metrics. Metrics with the same `group` value (e.g. `bp_systolic`/`bp_diastolic` both have `group="blood_pressure"`) are rendered side-by-side in the Track tab. Unknown metrics get a safe fallback via `get_metric_config()`.

## Database Schema (Supabase / SQLite)

Six tables: `users`, `metrics`, `medications`, `documents`, `personal_info`, `wearables`. Full schema in `kaki_care_schema001.sql`; SQLite equivalent embedded in `utils/sqlite_db.py`.

- `metrics` and `medications` have UNIQUE on `(user_id, date)` — writes always use upsert
- `wearables` allows multiple entries per day; queries fetch the latest by `created_at`
- `users.disease_profile` (JSONB/TEXT-JSON) is the source of truth for tracked metrics, thresholds, symptom options, and medication schedule

## n8n Workflows (4 total)

1. **Onboarding** (webhook) — PDF OCR → AI extracts disease profile → inserts `users`, `documents`, `medications`. Reference export: `KAKI Care - 1. Patient Onboarding.json`
2. **Health Check** (cron every 6h + callable as tool) — queries all patient data → AI compares against thresholds → returns alert or null. Reused by both scheduler and chatbot
3. **Chatbot** (webhook) — tools: `health_check`, `get_patient_context`, `log_notable_event`. No file uploads; directs vital input to Track tab
4. **Export/Doctor Summary** (webhook) — date-range query → AI generates SOAP markdown with flagged items

The chatbot integration point is `tabs/chat.py:_get_response()` — replace the stub with an n8n webhook POST.
The doctor summary integration point is `tabs/doctor.py` — replace `SOAP_SUMMARY`/`FLAGGED_ITEMS` constants with an n8n Export webhook call.

## Demo Scenario

Marcus Chen (67yo, CHF NYHA Class II). Mock data in `kaki_care_mock_marcus001.sql` (Supabase) and embedded in `utils/sqlite_db.py` (SQLite). Data covers Mar 5–18, 2026 with a deliberate decompensation signal: +2.3 kg weight gain Mar 10→16, SpO₂ dip to 91%, missed Furosemide doses Mar 13–14, progressive fatigue/ankle swelling/dyspnea/orthopnea. Recovery trend begins Mar 17.

## Key Design Decisions

- **Thresholds stored as text** — AI interprets flexibility; no hardcoded comparison logic
- **`personal_info`: AI-extracted only** — not a chat log; only clinically notable events
- **Wearables: raw API JSON** — stored verbatim; AI parses as needed
- **Medication schedule vs. adherence separation** — schedule in `users.disease_profile`, daily adherence in `medications`
