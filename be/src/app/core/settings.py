from typing import Literal
from urllib.parse import quote

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", frozen=True
    )

    app_name: str = Field(default="API", min_length=1)
    service_version: str = Field(default="0.1.0", min_length=1)
    app_environment: str = Field(default="local", min_length=1, max_length=64)
    server_host: str = Field(default="127.0.0.1", min_length=1)
    server_port: int = Field(default=8000, ge=1, le=65535)
    shutdown_timeout_seconds: int = Field(default=15, ge=1, le=300)
    log_level: Literal["debug", "info", "warning", "error", "critical"] = "info"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    db_host: str = Field(default="localhost", min_length=1)
    db_port: int = Field(default=5433, ge=1, le=65535)
    db_name: str = Field(default="app", min_length=1)
    db_username: str = Field(default="app", min_length=1)
    db_password: str = Field(default="app", repr=False)
    db_pool_size: int = Field(default=4, ge=1, le=100)
    db_pool_max_overflow: int = Field(default=0, ge=0, le=100)
    db_pool_timeout_seconds: float = Field(default=2, gt=0, le=60)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """asyncpg SQLAlchemy URL built from the individual DB_* settings."""
        username = quote(self.db_username, safe="")
        password = quote(self.db_password, safe="")
        return (
            f"postgresql+asyncpg://{username}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
