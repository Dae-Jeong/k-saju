import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import Settings


async def test_pgvector_extension_is_installed(
    dev_database_settings: Settings, db_available: bool
) -> None:
    if not db_available:
        pytest.skip("saju-postgres(5433)에 연결할 수 없습니다.")

    engine = create_async_engine(dev_database_settings.database_url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(
                text(
                    "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
                )
            )
            row = result.first()
    finally:
        await engine.dispose()

    assert row is not None, "vector extension is not installed; run `make migrate`"
