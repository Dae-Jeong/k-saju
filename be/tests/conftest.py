import asyncio
import os
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import Settings

# Settings에 기본값이 없는 필수 키들의 로컬 개발용 값. 실제 .env 파일이 아니라
# monkeypatch로만 주입합니다 — 테스트는 개발자의 .env에 의존하지 않습니다.
REQUIRED_ENV: dict[str, str] = {
    "APP_ENVIRONMENT": "local",
    "DB_HOST": "localhost",
    "DB_PORT": "5433",
    "DB_NAME": "saju",
    "DB_USERNAME": "app",
    "DB_PASSWORD": "app",
}


@pytest.fixture(autouse=True)
def isolate_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """개인 환경 설정과 프로젝트 .env가 테스트에 유입되지 않게 합니다."""
    monkeypatch.chdir(tmp_path)
    for name in tuple(os.environ):
        if name.lower() in Settings.model_fields:
            monkeypatch.delenv(name)


@pytest.fixture
def required_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """필수 환경변수를 로컬 개발 기본값으로 채웁니다 (monkeypatch 경유)."""
    for key, value in REQUIRED_ENV.items():
        monkeypatch.setenv(key, value)
    return dict(REQUIRED_ENV)


@pytest.fixture
def dev_database_settings(required_env: dict[str, str]) -> Settings:
    """로컬 개발 Postgres(saju-postgres, 5433)를 가리키는 Settings입니다.

    별도 테스트 DB는 두지 않습니다 — 이 컨테이너가 없거나(예: CI) 꺼져 있으면
    DB 의존 테스트는 실패 대신 깔끔히 skip합니다.
    """
    return Settings(db_name="saju")


@pytest.fixture
def db_available(dev_database_settings: Settings) -> bool:
    """개발 DB에 연결 가능한지 확인합니다. 불가능하면 관련 테스트를 skip합니다."""

    async def check() -> bool:
        engine = create_async_engine(dev_database_settings.database_url)
        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            await engine.dispose()

    return asyncio.run(check())
