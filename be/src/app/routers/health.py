from typing import cast

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.http.errors import problem_response
from app.schemas.responses import ErrorCode

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/ready", responses={503: {"description": "Not ready"}})
async def readiness(request: Request) -> JSONResponse:
    """Liveness only reports the process is up; readiness actively pings the DB."""
    if not request.app.state.ready:
        return problem_response(
            request,
            status=503,
            code=ErrorCode.DATABASE_UNAVAILABLE,
            headers={"Retry-After": "1"},
        )
    factory = cast(async_sessionmaker[AsyncSession], request.app.state.session_factory)
    try:
        async with factory() as session:
            await session.execute(text("SELECT 1"))
    except SQLAlchemyError, OSError:
        return problem_response(
            request,
            status=503,
            code=ErrorCode.DATABASE_UNAVAILABLE,
            headers={"Retry-After": "1"},
        )
    return JSONResponse({"status": "ready"}, status_code=200)
