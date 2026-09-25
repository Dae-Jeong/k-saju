import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from app.bootstrap.app import create_app
from app.core.settings import Settings


def test_database_url_is_built_from_parts() -> None:
    settings = Settings(
        db_host="db.example",
        db_port=5555,
        db_name="mydb",
        db_username="user",
        db_password="p@ss/word",
    )
    assert settings.database_url == (
        "postgresql+asyncpg://user:p%40ss%2Fword@db.example:5555/mydb"
    )


def test_invalid_server_port_raises() -> None:
    with pytest.raises(ValidationError):
        Settings(server_port=0)


def test_environment_overrides_dotenv(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    (tmp_path / ".env").write_text("APP_NAME=from-file\nSERVER_PORT=19080\n")
    monkeypatch.setenv("APP_NAME", "from-environment")
    settings = Settings()
    assert settings.app_name == "from-environment"
    assert settings.server_port == 19080


def test_app_settings_are_independent() -> None:
    first = create_app(Settings(app_name="first", service_version="1"))
    second = create_app(Settings(app_name="second", service_version="2"))
    assert first.title == "first"
    assert second.title == "second"
    assert second.version == "2"


def test_invalid_environment_exits_without_leaking_input(tmp_path: Path) -> None:
    secret = "synthetic-secret-value"
    result = subprocess.run(
        [sys.executable, "-m", "app.run"],
        cwd=tmp_path,
        env={**os.environ, "SERVER_PORT": secret},
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 1
    assert "server_port: int_parsing" in result.stderr
    assert secret not in result.stderr + result.stdout
