import asyncio
import os
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import Settings


@pytest.fixture(autouse=True)
def isolate_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """개인 환경 설정과 프로젝트 .env가 테스트에 유입되지 않게 합니다."""
    monkeypatch.chdir(tmp_path)
    for name in tuple(os.environ):
        if name.lower() in Settings.model_fields:
            monkeypatch.delenv(name)


@pytest.fixture
def dev_database_settings() -> Settings:
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
