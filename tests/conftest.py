from fastapi.testclient import TestClient

from src.app import app


def create_test_client() -> TestClient:
    return TestClient(app)
