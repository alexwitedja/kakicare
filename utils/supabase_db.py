"""Supabase backend — called by db.py when DB_BACKEND=supabase."""

from supabase import Client


def get_user_name(client: Client, user_id: int) -> str:
    result = (
        client.table("users")
        .select("name")
        .eq("id", user_id)
        .single()
        .execute()
    )
    if not result.data:
        raise RuntimeError(f"No user found with id={user_id}.")
    return result.data["name"]


def get_latest_wearables(client: Client, user_id: int, date: str) -> dict | None:
    rows = (
        client.table("wearables")
        .select("raw_data, created_at")
        .eq("user_id", user_id)
        .gte("created_at", f"{date}T00:00:00")
        .lt("created_at", f"{date}T23:59:59")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
        .data
    )
    return rows[0]["raw_data"] if rows else None


def get_disease_profile(client: Client, user_id: int) -> dict:
    try:
        result = (
            client.table("users")
            .select("disease_profile")
            .eq("id", user_id)
            .single()
            .execute()
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch disease profile: {e}") from e
    if not result.data:
        raise RuntimeError(f"No user found with id={user_id}.")
    return result.data["disease_profile"]


def get_today_metrics(client: Client, user_id: int, today: str) -> dict | None:
    try:
        result = (
            client.table("metrics")
            .select("readings")
            .eq("user_id", user_id)
            .eq("date", today)
            .maybe_single()
            .execute()
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch today's metrics: {e}") from e
    return result.data["readings"] if result.data else None


def get_today_medications(client: Client, user_id: int, today: str) -> dict | None:
    try:
        result = (
            client.table("medications")
            .select("taken")
            .eq("user_id", user_id)
            .eq("date", today)
            .maybe_single()
            .execute()
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch today's medications: {e}") from e
    return result.data["taken"] if result.data else None


def get_recent_metrics(client: Client, user_id: int, days: int = 7) -> list[dict]:
    rows = (
        client.table("metrics")
        .select("date, readings")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .limit(days)
        .execute()
        .data
    )
    return [{"date": r["date"], **r["readings"]} for r in reversed(rows)]


def upsert_metrics(client: Client, user_id: int, today: str, readings: dict) -> None:
    try:
        client.table("metrics").upsert(
            {"user_id": user_id, "date": today, "readings": readings},
            on_conflict="user_id,date",
        ).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to save metrics: {e}") from e


def upsert_medications(client: Client, user_id: int, today: str, taken: dict) -> None:
    try:
        client.table("medications").upsert(
            {"user_id": user_id, "date": today, "taken": taken},
            on_conflict="user_id,date",
        ).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to save medications: {e}") from e
