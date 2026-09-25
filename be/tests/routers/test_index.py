from fastapi.testclient import TestClient

from app.bootstrap.app import create_app
from app.core.settings import Settings


def test_index_returns_success_envelope(required_env: dict[str, str]) -> None:
    app = create_app(Settings())
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": {"message": "Hello, API!"}}


def test_unknown_route_returns_problem_details(required_env: dict[str, str]) -> None:
    app = create_app(Settings())
    with TestClient(app) as client:
        response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["code"] == "NOT_FOUND"
    assert "X-Request-ID" in response.headers
