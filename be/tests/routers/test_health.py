import pytest
from fastapi.testclient import TestClient

from app.bootstrap.app import create_app
from app.core.settings import Settings


def test_liveness_is_always_ok() -> None:
    app = create_app(Settings())
    with TestClient(app) as client:
        response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_returns_problem_when_database_unreachable() -> None:
    # 예약된 저권한 포트로 강제해 로컬 Docker 실행 여부와 무관하게 재현합니다.
    app = create_app(Settings(db_port=1))
    with TestClient(app) as client:
        response = client.get("/health/ready")
    assert response.status_code == 503
    assert response.headers["content-type"] == "application/problem+json"
    body = response.json()
    assert body["code"] == "DATABASE_UNAVAILABLE"
    assert response.headers["Retry-After"] == "1"


def test_readiness_returns_ok_when_database_reachable(
    dev_database_settings: Settings, db_available: bool
) -> None:
    if not db_available:
        pytest.skip("saju-postgres(5433)에 연결할 수 없습니다.")
    app = create_app(dev_database_settings)
    with TestClient(app) as client:
        response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
