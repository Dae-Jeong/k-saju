from functools import partial

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.bootstrap.contracts import PrepareResources
from app.bootstrap.lifespan import create_lifespan, prepare_resources
from app.core.clock import system_clock
from app.core.contracts import Clock, LogContext
from app.core.settings import Settings
from app.http.errors import (
    http_error,
    internal_error,
    problem_openapi,
    validation_error,
)
from app.routers.health import router as health_router
from app.routers.index import router as index_router


def create_app(
    settings: Settings,
    *,
    clock: Clock = system_clock,
    prepare: PrepareResources | None = None,
) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.service_version,
        lifespan=create_lifespan(
            prepare
            if prepare is not None
            else partial(prepare_resources, settings=settings)
        ),
    )
    app.state.clock = clock
    app.state.ready = False
    app.state.log_context = LogContext(
        settings.app_name, settings.service_version, settings.app_environment
    )
    app.add_exception_handler(RequestValidationError, validation_error)
    app.add_exception_handler(HTTPException, http_error)
    app.add_exception_handler(Exception, internal_error)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(index_router)
    app.include_router(health_router)
    # FastAPI가 지원하는 인스턴스별 OpenAPI 함수 교체입니다. self는 partial로 고정합니다.
    app.openapi = partial(problem_openapi, app, app.openapi)  # ty: ignore[invalid-assignment]
    return app
