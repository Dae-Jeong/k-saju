import sys

import uvicorn
from pydantic import ValidationError

from app.bootstrap.app import create_app
from app.core.contracts import LogContext
from app.core.logging import configure_logging
from app.core.settings import Settings


def main() -> None:
    try:
        settings = Settings()
    except ValidationError as error:
        # 환경값 자체는 출력하지 않습니다 — 키 이름만 나열합니다.
        keys: list[str] = []
        for detail in error.errors(include_input=False, include_context=False):
            field = detail["loc"][0] if detail["loc"] else "settings"
            if field not in Settings.model_fields:
                field = "settings"
            key = str(field).upper()
            if key not in keys:
                keys.append(key)
        print(
            f"Missing or invalid environment variables: {', '.join(keys)}",
            file=sys.stderr,
        )
        raise SystemExit(1) from None

    configure_logging(
        LogContext(
            settings.app_name, settings.service_version, settings.app_environment
        ),
        settings.log_level,
    )
    app = create_app(settings)
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level=settings.log_level,
        access_log=False,
        log_config=None,
        workers=1,
        timeout_graceful_shutdown=settings.shutdown_timeout_seconds,
    )


if __name__ == "__main__":
    main()
