from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

type Clock = Callable[[], datetime]


@dataclass(frozen=True)
class LogContext:
    service_name: str
    service_version: str
    environment: str
