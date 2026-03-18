METRIC_CONFIG = {
    "daily_weight": {"label": "Weight", "unit": "kg", "type": "float", "step": 0.1, "min": 20.0, "max": 300.0, "default": 70.0, "group": None},
    "heart_rate":   {"label": "Heart Rate", "unit": "bpm", "type": "int", "step": 1, "min": 30, "max": 250, "default": 70, "group": None},
    "spo2":         {"label": "SpO₂", "unit": "%", "type": "int", "step": 1, "min": 0, "max": 100, "default": 98, "group": None},
    "bp_systolic":  {"label": "Systolic BP", "unit": "mmHg", "type": "int", "step": 1, "min": 60, "max": 250, "default": 120, "group": "blood_pressure"},
    "bp_diastolic": {"label": "Diastolic BP", "unit": "mmHg", "type": "int", "step": 1, "min": 40, "max": 150, "default": 80, "group": "blood_pressure"},
}

MOOD_EMOJI_MAP = {
    "great": "😄 Great",
    "good": "🙂 Good",
    "okay": "😐 Okay",
    "bad": "😟 Bad",
    "struggling": "😢 Struggling",
}

def get_metric_config(metric_name: str) -> dict:
    """Returns known config or a safe fallback for unknown metrics."""
    return METRIC_CONFIG.get(metric_name, {
        "label": metric_name.replace("_", " ").title(),
        "unit": "",
        "type": "float",
        "step": 0.1,
        "min": 0.0,
        "max": 9999.0,
        "default": 0.0,
        "group": None,
    })
