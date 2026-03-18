"""
Public database interface for KAKI Care.

Routes to SQLite or Supabase based on DB_BACKEND env var.
  DB_BACKEND=sqlite   → local kaki_care.db (default)
  DB_BACKEND=supabase → Supabase (requires SUPABASE_URL + SUPABASE_KEY)
"""

import os
import sqlite3

import streamlit as st

_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()


# ---------------------------------------------------------------------------
# Client factory
# ---------------------------------------------------------------------------

def get_db_client():
    """Return the appropriate DB client based on DB_BACKEND."""
    if _BACKEND == "supabase":
        return _get_supabase_client()
    return _get_sqlite_client()


@st.cache_resource
def _get_supabase_client():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_KEY must be set when DB_BACKEND=supabase."
        )
    return create_client(url, key)


def _get_sqlite_client():
    from utils.sqlite_db import get_sqlite_connection
    return get_sqlite_connection()


def _is_sqlite(client) -> bool:
    return isinstance(client, sqlite3.Connection)


# ---------------------------------------------------------------------------
# Profile normalization
# The raw disease_profile JSONB uses a nested structure:
#   { "diseases": [{ "metrics": [...], "symptom_options": [...], ... }],
#     "medications": [...] }
# We flatten it so callers always see:
#   tracked_metrics, symptom_options, mood_options, medication_schedule
# ---------------------------------------------------------------------------

def _normalize_profile(raw: dict) -> dict:
    if "diseases" not in raw:
        return raw  # already flat or unknown shape
    disease = raw["diseases"][0] if raw["diseases"] else {}
    return {
        "tracked_metrics": disease.get("metrics", []),
        "mood_options": disease.get("mood_options", ["great", "good", "okay", "bad", "struggling"]),
        "symptom_options": disease.get("symptom_options", []),
        "medication_schedule": raw.get("medications", []),
        # preserve everything else (thresholds, comorbidities, etc.)
        "diseases": raw["diseases"],
    }


# ---------------------------------------------------------------------------
# Public API — same signature regardless of backend
# ---------------------------------------------------------------------------

def get_user_name(client, user_id: int) -> str:
    if _is_sqlite(client):
        from utils.sqlite_db import get_user_name as _get
    else:
        from utils.supabase_db import get_user_name as _get
    return _get(client, user_id)


def get_latest_wearables(client, user_id: int, date: str) -> dict | None:
    if _is_sqlite(client):
        from utils.sqlite_db import get_latest_wearables as _get
    else:
        from utils.supabase_db import get_latest_wearables as _get
    return _get(client, user_id, date)


def get_disease_profile(client, user_id: int) -> dict:
    if _is_sqlite(client):
        from utils.sqlite_db import get_disease_profile as _get
    else:
        from utils.supabase_db import get_disease_profile as _get
    return _normalize_profile(_get(client, user_id))


def get_today_metrics(client, user_id: int, today: str) -> dict | None:
    if _is_sqlite(client):
        from utils.sqlite_db import get_today_metrics as _get
    else:
        from utils.supabase_db import get_today_metrics as _get
    return _get(client, user_id, today)


def get_today_medications(client, user_id: int, today: str) -> dict | None:
    if _is_sqlite(client):
        from utils.sqlite_db import get_today_medications as _get
    else:
        from utils.supabase_db import get_today_medications as _get
    return _get(client, user_id, today)


def get_recent_metrics(client, user_id: int, days: int = 7) -> list[dict]:
    if _is_sqlite(client):
        from utils.sqlite_db import get_recent_metrics as _get
    else:
        from utils.supabase_db import get_recent_metrics as _get
    return _get(client, user_id, days)


def upsert_metrics(client, user_id: int, today: str, readings: dict) -> None:
    if _is_sqlite(client):
        from utils.sqlite_db import upsert_metrics as _fn
    else:
        from utils.supabase_db import upsert_metrics as _fn
    _fn(client, user_id, today, readings)


def upsert_medications(client, user_id: int, today: str, taken: dict) -> None:
    if _is_sqlite(client):
        from utils.sqlite_db import upsert_medications as _fn
    else:
        from utils.supabase_db import upsert_medications as _fn
    _fn(client, user_id, today, taken)
