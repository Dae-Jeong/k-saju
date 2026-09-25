from typing import Literal
from urllib.parse import quote

from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Process env vars only — no .env file is ever read here.

    Local values come from the root `.env` (loaded into the process env by
    the Makefile before this runs); deployed values come from the server
    runtime env. Required fields have no default: a missing or invalid one
    fails fast with a `ValidationError` listing every offending key.
    """

    model_config = SettingsConfigDict(frozen=True)

    # Required — no sensible default, must come from the environment.
    app_environment: str = Field(min_length=1, max_length=64)
    db_host: str = Field(min_length=1)
    db_port: int = Field(ge=1, le=65535)
    db_name: str = Field(min_length=1)
    db_username: str = Field(min_length=1)
    db_password: SecretStr

    # Optional tuning values — genuinely safe to default.
    app_name: str = Field(default="API", min_length=1)
    service_version: str = Field(default="0.1.0", min_length=1)
    server_host: str = Field(default="127.0.0.1", min_length=1)
    server_port: int = Field(default=8000, ge=1, le=65535)
    shutdown_timeout_seconds: int = Field(default=15, ge=1, le=300)
    log_level: Literal["debug", "info", "warning", "error", "critical"] = "info"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    db_pool_size: int = Field(default=4, ge=1, le=100)
    db_pool_max_overflow: int = Field(default=0, ge=0, le=100)
    db_pool_timeout_seconds: float = Field(default=2, gt=0, le=60)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """asyncpg SQLAlchemy URL built from the individual DB_* settings."""
        username = quote(self.db_username, safe="")
        password = quote(self.db_password.get_secret_value(), safe="")
        return (
            f"postgresql+asyncpg://{username}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
