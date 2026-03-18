"""Quick test script for n8n webhook endpoints."""

import json
import requests

BASE_URL = "https://n8n.truehorizonai.com/webhook"


def test_chatting():
    print("=== POST /chatting ===")
    url = f"{BASE_URL}/chatting"
    payload = {"id": 1, "chatInput": "Hello, how am I doing today?"}
    try:
        resp = requests.post(url, json=payload, timeout=30)
        print(f"Status : {resp.status_code}")
        print(f"Headers: {dict(resp.headers)}")
        try:
            print(f"Body   : {json.dumps(resp.json(), indent=2)}")
        except Exception:
            print(f"Body   : {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR  : {e}")
    print()


def test_reportgen():
    print("=== GET /reportgen ===")
    url = f"{BASE_URL}/reportgen"
    params = {"user_id": 1, "days": 14}
    try:
        resp = requests.get(url, params=params, timeout=30)
        print(f"Status : {resp.status_code}")
        print(f"Headers: {dict(resp.headers)}")
        try:
            print(f"Body   : {json.dumps(resp.json(), indent=2)}")
        except Exception:
            print(f"Body   : {resp.text}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR  : {e}")
    print()


if __name__ == "__main__":
    test_chatting()
    test_reportgen()
