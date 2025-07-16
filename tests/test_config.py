from src.config import Settings

def test_default_database_url(monkeypatch):
    """
    Test that the Settings class correctly reads the DATABASE_URL
    environment variable and sets the debug flag to True by default.
    """
    # Set the DATABASE_URL environment variable for the test
    monkeypatch.setenv("DATABASE_URL", "sqlite:///./foo.db")
    # Instantiate the Settings object
    s = Settings()
    # Check that the database_url ends with 'foo.db'
    assert str(s.database_url).endswith("foo.db")
    # Check that debug is True by default
    assert s.debug is True

def test_debug_flag(monkeypatch):
    """
    Test that the Settings class correctly reads the DEBUG
    environment variable and sets the debug flag accordingly.
    """
    # Set the DEBUG environment variable for the test
    monkeypatch.setenv("DEBUG", "true")
    # Instantiate the Settings object
    s = Settings()
    # Check that debug is set to True
    assert s.debug is True