"""SQLite backend — mirrors the Supabase interface used by db.py."""

import json
import os
import sqlite3

import streamlit as st

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    age     INTEGER,
    disease_profile TEXT  -- stored as JSON
);

CREATE TABLE IF NOT EXISTS metrics (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date    TEXT NOT NULL,
    readings TEXT,  -- stored as JSON
    UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS medications (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date    TEXT NOT NULL,
    taken   TEXT,  -- stored as JSON
    UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS documents (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER REFERENCES users(id) ON DELETE CASCADE,
    document_name TEXT NOT NULL,
    content       TEXT
);

CREATE TABLE IF NOT EXISTS personal_info (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER REFERENCES users(id) ON DELETE CASCADE,
    timestamp      TEXT DEFAULT (datetime('now')),
    extracted_info TEXT
);

CREATE TABLE IF NOT EXISTS wearables (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id) ON DELETE CASCADE,
    raw_data   TEXT,  -- stored as JSON
    created_at TEXT DEFAULT (datetime('now'))
);
"""

_MARCUS_PROFILE = {
    "diseases": [
        {
            "name": "CHF",
            "nyha_class": "II",
            "ejection_fraction": "40%",
            "comorbidities": ["hypertension", "type 2 diabetes"],
            "metrics": ["daily_weight", "heart_rate", "spo2", "bp_systolic", "bp_diastolic"],
            "thresholds": {
                "daily_weight": "gain >2kg in 2 days",
                "spo2": "below 94%",
                "heart_rate": "resting HR >100 bpm or >20% above baseline",
                "bp_systolic": "above 180 or below 90",
                "bp_diastolic": "above 120 or below 60",
            },
            "symptom_options": [
                "shortness_of_breath", "ankle_swelling", "fatigue",
                "chest_discomfort", "dizziness", "night_coughing", "difficulty_lying_flat",
            ],
            "mood_options": ["great", "good", "okay", "bad", "struggling"],
        }
    ],
    "medications": [
        {"name": "Lisinopril",  "dosage": "10mg",  "times": ["08:00"]},
        {"name": "Carvedilol",  "dosage": "25mg",  "times": ["08:00"]},
        {"name": "Furosemide",  "dosage": "40mg",  "times": ["08:00", "14:00", "20:00"]},
    ],
}

_MARCUS_METRICS = [
    ("2026-03-05", {"weight": 75.2, "bp_systolic": 128, "bp_diastolic": 82, "mood": "good", "symptoms": []}),
    ("2026-03-06", {"weight": 75.3, "bp_systolic": 130, "bp_diastolic": 80, "mood": "good", "symptoms": []}),
    ("2026-03-07", {"weight": 75.1, "bp_systolic": 126, "bp_diastolic": 78, "mood": "great", "symptoms": []}),
    ("2026-03-08", {"weight": 75.4, "bp_systolic": 132, "bp_diastolic": 84, "mood": "okay", "symptoms": ["fatigue"]}),
    ("2026-03-09", {"weight": 75.2, "bp_systolic": 129, "bp_diastolic": 81, "mood": "good", "symptoms": []}),
    ("2026-03-10", {"weight": 75.5, "bp_systolic": 131, "bp_diastolic": 80, "mood": "good", "symptoms": []}),
    ("2026-03-11", {"weight": 75.3, "bp_systolic": 127, "bp_diastolic": 79, "mood": "good", "symptoms": []}),
    ("2026-03-12", {"weight": 75.6, "bp_systolic": 133, "bp_diastolic": 82, "mood": "okay", "symptoms": []}),
    ("2026-03-13", {"weight": 75.8, "bp_systolic": 135, "bp_diastolic": 85, "mood": "okay", "symptoms": ["fatigue"]}),
    ("2026-03-14", {"weight": 76.2, "bp_systolic": 138, "bp_diastolic": 86, "mood": "bad",  "symptoms": ["fatigue", "ankle_swelling"]}),
    ("2026-03-15", {"weight": 77.0, "bp_systolic": 142, "bp_diastolic": 88, "mood": "bad",  "symptoms": ["fatigue", "ankle_swelling", "shortness_of_breath"]}),
    ("2026-03-16", {"weight": 77.8, "bp_systolic": 145, "bp_diastolic": 90, "mood": "struggling", "symptoms": ["fatigue", "ankle_swelling", "shortness_of_breath", "difficulty_lying_flat"]}),
    ("2026-03-17", {"weight": 76.5, "bp_systolic": 136, "bp_diastolic": 84, "mood": "okay", "symptoms": ["fatigue", "ankle_swelling"]}),
    ("2026-03-18", {"weight": 75.8, "bp_systolic": 132, "bp_diastolic": 82, "mood": "okay", "symptoms": ["fatigue"]}),
]

_FULL_TAKEN = {"Lisinopril": {"08:00": True}, "Carvedilol": {"08:00": True}, "Furosemide": {"08:00": True, "14:00": True, "20:00": True}}

_MARCUS_WEARABLES = [
    ("2026-03-12", {"heart_rate": 76, "spo2": 97, "steps": 4200, "sleep_hours": 7.2}),
    ("2026-03-13", {"heart_rate": 78, "spo2": 97, "steps": 3900, "sleep_hours": 6.8}),
    ("2026-03-14", {"heart_rate": 88, "spo2": 93, "steps": 2800, "sleep_hours": 6.1}),
    ("2026-03-15", {"heart_rate": 92, "spo2": 92, "steps": 1800, "sleep_hours": 5.5}),
    ("2026-03-16", {"heart_rate": 96, "spo2": 91, "steps": 1200, "sleep_hours": 4.9}),
    ("2026-03-17", {"heart_rate": 80, "spo2": 94, "steps": 2500, "sleep_hours": 6.3}),
    ("2026-03-18", {"heart_rate": 74, "spo2": 96, "steps": 3100, "sleep_hours": 7.0}),
]

_MARCUS_MEDICATIONS = [
    ("2026-03-05", _FULL_TAKEN),
    ("2026-03-06", _FULL_TAKEN),
    ("2026-03-07", _FULL_TAKEN),
    ("2026-03-08", _FULL_TAKEN),
    ("2026-03-09", _FULL_TAKEN),
    ("2026-03-10", _FULL_TAKEN),
    ("2026-03-11", _FULL_TAKEN),
    ("2026-03-12", _FULL_TAKEN),
    ("2026-03-13", {"Lisinopril": {"08:00": True}, "Carvedilol": {"08:00": True}, "Furosemide": {"08:00": True,  "14:00": True,  "20:00": False}}),
    ("2026-03-14", {"Lisinopril": {"08:00": True}, "Carvedilol": {"08:00": True}, "Furosemide": {"08:00": True,  "14:00": False, "20:00": False}}),
    ("2026-03-15", _FULL_TAKEN),
    ("2026-03-16", _FULL_TAKEN),
    ("2026-03-17", _FULL_TAKEN),
    ("2026-03-18", _FULL_TAKEN),
]


def _seed(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        # Users already seeded — backfill wearables if missing
        cur.execute("SELECT COUNT(*) FROM wearables")
        if cur.fetchone()[0] == 0:
            cur.execute("SELECT id FROM users LIMIT 1")
            row = cur.fetchone()
            if row:
                uid = row[0]
                cur.executemany(
                    "INSERT INTO wearables (user_id, raw_data, created_at) VALUES (?, ?, ?)",
                    [(uid, json.dumps(r), f"{d}T08:00:00") for d, r in _MARCUS_WEARABLES],
                )
                conn.commit()
        return

    cur.execute(
        "INSERT INTO users (name, age, disease_profile) VALUES (?, ?, ?)",
        ("Marcus", 67, json.dumps(_MARCUS_PROFILE)),
    )
    user_id = cur.lastrowid

    cur.executemany(
        "INSERT INTO metrics (user_id, date, readings) VALUES (?, ?, ?)",
        [(user_id, d, json.dumps(r)) for d, r in _MARCUS_METRICS],
    )
    cur.executemany(
        "INSERT INTO medications (user_id, date, taken) VALUES (?, ?, ?)",
        [(user_id, d, json.dumps(t)) for d, t in _MARCUS_MEDICATIONS],
    )
    cur.executemany(
        "INSERT INTO wearables (user_id, raw_data, created_at) VALUES (?, ?, ?)",
        [(user_id, json.dumps(r), f"{d}T08:00:00") for d, r in _MARCUS_WEARABLES],
    )
    conn.commit()


@st.cache_resource
def get_sqlite_connection() -> sqlite3.Connection:
    path = os.getenv("SQLITE_PATH", "kaki_care.db")
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    _seed(conn)
    return conn


# --- CRUD ---

def get_user_name(conn: sqlite3.Connection, user_id: int) -> str:
    row = conn.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        raise RuntimeError(f"No user found with id={user_id}.")
    return row["name"]


def get_latest_wearables(conn: sqlite3.Connection, user_id: int, date: str) -> dict | None:
    row = conn.execute(
        "SELECT raw_data FROM wearables WHERE user_id = ? AND date(created_at) = ? ORDER BY created_at DESC LIMIT 1",
        (user_id, date),
    ).fetchone()
    return json.loads(row["raw_data"]) if row else None


def get_disease_profile(conn: sqlite3.Connection, user_id: int) -> dict:
    try:
        row = conn.execute(
            "SELECT disease_profile FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch disease profile: {e}") from e
    if not row:
        raise RuntimeError(f"No user found with id={user_id}.")
    return json.loads(row["disease_profile"])


def get_today_metrics(conn: sqlite3.Connection, user_id: int, today: str) -> dict | None:
    try:
        row = conn.execute(
            "SELECT readings FROM metrics WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch today's metrics: {e}") from e
    return json.loads(row["readings"]) if row else None


def get_today_medications(conn: sqlite3.Connection, user_id: int, today: str) -> dict | None:
    try:
        row = conn.execute(
            "SELECT taken FROM medications WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch today's medications: {e}") from e
    return json.loads(row["taken"]) if row else None


def get_recent_metrics(conn: sqlite3.Connection, user_id: int, days: int = 7) -> list[dict]:
    rows = conn.execute(
        "SELECT date, readings FROM metrics WHERE user_id = ? ORDER BY date DESC LIMIT ?",
        (user_id, days),
    ).fetchall()
    return [{"date": r["date"], **json.loads(r["readings"])} for r in reversed(rows)]


def upsert_metrics(conn: sqlite3.Connection, user_id: int, today: str, readings: dict) -> None:
    try:
        conn.execute(
            "INSERT INTO metrics (user_id, date, readings) VALUES (?, ?, ?)"
            " ON CONFLICT(user_id, date) DO UPDATE SET readings = excluded.readings",
            (user_id, today, json.dumps(readings)),
        )
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Failed to save metrics: {e}") from e


def upsert_medications(conn: sqlite3.Connection, user_id: int, today: str, taken: dict) -> None:
    try:
        conn.execute(
            "INSERT INTO medications (user_id, date, taken) VALUES (?, ?, ?)"
            " ON CONFLICT(user_id, date) DO UPDATE SET taken = excluded.taken",
            (user_id, today, json.dumps(taken)),
        )
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Failed to save medications: {e}") from e
