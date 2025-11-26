import pytest
from fastapi.testclient import TestClient
from src.app import app, clear_tasks


@pytest.fixture(autouse=True) #autouse=True → cette fixture s’exécute automatiquement pour tous les tests
def clean_tasks():
    """
    Clear all tasks before each test.
    This ensures tests don't interfere with each other.

    yield :
    Ici, tout ce qui est avant yield s’exécute avant le test
    Tout ce qui est après yield s’exécute après le test (cleanup).
    """
    clear_tasks()
    yield
    clear_tasks()


@pytest.fixture
def client():
    """
    Provide a test client for making API requests.

    Usage in tests:
        def test_something(client):
            response = client.get("/tasks")
            assert response.status_code == 200
    """
    with TestClient(app) as test_client:
        yield test_client

def pytest_configure(config):
 """Enregistre les markers personnalisés"""
 config.addinivalue_line(
 "markers",
 "e2e: mark test as end-to-end test (slow)"
 )
