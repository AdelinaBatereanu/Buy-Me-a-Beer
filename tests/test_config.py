import os
from src.config import Settings

def test_default_database_url(monkeypatch):
    # Simulate .env value
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./foo.db")
    s = Settings()
    assert str(s.database_url).endswith("foo.db")
    assert s.debug is True 

def test_debug_flag(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    s = Settings()
    assert s.debug is True