"""
Pytest konfigurasjon og fixtures
"""
import pytest
import sys
from pathlib import Path

# Legg til prosjekt-stier
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "SANDKASSE" / "07_Sandkasse_SelfHealing"))


def pytest_configure(config):
    """Konfigurer pytest"""
    config.addinivalue_line("markers", "unit: Unit tester (raske, isolerte)")
    config.addinivalue_line("markers", "integration: Integrasjonstester (med avhengigheter)")
    config.addinivalue_line("markers", "slow: Treige tester (>1s)")
    config.addinivalue_line("markers", "async: Asynkrone tester")


@pytest.fixture(scope="session")
def event_loop():
    """Fixture for async tester"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir(tmp_path):
    """Temporær mappe for tester"""
    return tmp_path


@pytest.fixture
def mock_env(monkeypatch):
    """Mock miljøvariabler"""
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    monkeypatch.setenv("TESTING_MODE", "true")
