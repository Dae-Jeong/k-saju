from fastapi.testclient import TestClient

from app.bootstrap.app import create_app
from app.core.settings import Settings


def test_default_cors_origin_is_allowed() -> None:
    app = create_app(Settings())
    with TestClient(app) as client:
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_unlisted_cors_origin_is_not_allowed() -> None:
    app = create_app(Settings())
    with TestClient(app) as client:
        response = client.get("/", headers={"Origin": "http://evil.example"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_cors_origins_are_configurable() -> None:
    app = create_app(Settings(cors_origins=["http://custom.example"]))
    with TestClient(app) as client:
        response = client.get("/", headers={"Origin": "http://custom.example"})
    assert response.headers["access-control-allow-origin"] == "http://custom.example"
