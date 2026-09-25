import json
import logging
import sys
from datetime import UTC, datetime

from app.core.contracts import LogContext

MAX_LOG_BYTES = 16 * 1024


class JsonFormatter(logging.Formatter):
    def __init__(self, context: LogContext) -> None:
        super().__init__()
        self.context = context

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "@timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "log": {"level": record.levelname.lower(), "logger": record.name[:128]},
            "service": {
                "name": self.context.service_name[:128],
                "version": self.context.service_version[:128],
            },
            "app": {
                "environment": self.context.environment[:64],
                "log_schema_version": 1,
            },
            "message": record.getMessage()[:2048],
        }
        if record.exc_info is not None and record.exc_info[0] is not None:
            payload["error"] = {"type": record.exc_info[0].__name__[:128]}
        line = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        if len(line.encode("utf-8")) + 1 > MAX_LOG_BYTES:
            payload.pop("error", None)
            cast_app = payload["app"]
            assert isinstance(cast_app, dict)
            cast_app["truncated"] = True
            line = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        return line


class JsonHandler(logging.StreamHandler):
    """표준 handler의 출력 오류에서 원문 record·traceback 노출을 막습니다."""

    def handleError(self, record: logging.LogRecord) -> None:
        try:
            sys.stderr.write(
                '{"message":"logging.output_failed","log":{"level":"error"}}\n'
            )
            sys.stderr.flush()
        except Exception:
            # stdout·stderr 동시 장애에서는 보고를 보장할 수 없습니다.
            pass


def configure_logging(context: LogContext, level: str) -> None:
    """실행 진입점에서만 호출하며 타 도구 handler는 삭제하지 않습니다."""
    for name in ("app", "uvicorn"):
        logger = logging.getLogger(name)
        handler = next((h for h in logger.handlers if isinstance(h, JsonHandler)), None)
        if handler is None:
            handler = JsonHandler(sys.stdout)
            logger.addHandler(handler)
        handler.setFormatter(JsonFormatter(context))
        logger.setLevel(level.upper())
        logger.propagate = False
