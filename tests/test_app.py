from fastapi.testclient import TestClient
from src.app import app
from src.config import settings

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Buy Me a Beer" in resp.text

def test_success_page():
    resp = client.get("/success")
    assert resp.status_code == 200
    assert "Thank You" in resp.text

def test_cancel_page():
    resp = client.get("/cancel")
    assert resp.status_code == 200
    assert "Donation canceled" in resp.text

def test_list_donations_requires_api_key():
    resp = client.get("/donations/")
    assert resp.status_code == 422 or resp.status_code == 403  # Missing or invalid API key

def test_list_donations_with_api_key(monkeypatch):
    # Insert a dummy donation for testing
    from src.db import SessionLocal
    from src.crud import create_pending_donation
    db = SessionLocal()
    create_pending_donation(db, "Test", 1.0, "Test message")
    db.close()

    resp = client.get(
        "/donations/",
        headers={"X-API-Key": settings.admin_api_key}
    )
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)