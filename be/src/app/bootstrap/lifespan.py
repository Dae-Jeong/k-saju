from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bootstrap.contracts import Lifespan, PrepareResources
from app.core.database import create_engine
from app.core.settings import Settings


async def prepare_resources(
    app: FastAPI, stack: AsyncExitStack, *, settings: Settings
) -> None:
    """Create the DB engine without blocking startup on connectivity.

    Readiness (routers/health.py) probes the DB per request instead, so the
    app can start even while the database is unreachable.
    """
    engine = create_engine(settings)
    stack.push_async_callback(engine.dispose)
    app.state.engine = engine
    app.state.session_factory = async_sessionmaker(engine, expire_on_commit=False)
    stack.callback(delattr, app.state, "engine")
    stack.callback(delattr, app.state, "session_factory")


def create_lifespan(prepare: PrepareResources) -> Lifespan:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.ready = False
        stack = AsyncExitStack()
        try:
            await prepare(app, stack)
            app.state.ready = True
            yield
        except BaseException as error:
            # 취소와 초기화 실패도 자원을 정리한 뒤 원래 실패로 전파합니다.
            app.state.ready = False
            try:
                await stack.aclose()
            except BaseException as cleanup_error:
                raise error from cleanup_error
            raise
        else:
            app.state.ready = False
            await stack.aclose()

    return lifespan
