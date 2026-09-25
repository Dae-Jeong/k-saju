import os
import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch
from tests.conftest import REQUIRED_ENV

from app.bootstrap.app import create_app
from app.core.settings import Settings


def test_database_url_is_built_from_parts() -> None:
    settings = Settings(
        app_environment="local",
        db_host="db.example",
        db_port=5555,
        db_name="mydb",
        db_username="user",
        db_password="p@ss/word",
    )
    assert settings.database_url == (
        "postgresql+asyncpg://user:p%40ss%2Fword@db.example:5555/mydb"
    )


def test_invalid_server_port_raises(required_env: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        Settings(server_port=0)


def test_missing_required_vars_raise_with_all_field_names_listed() -> None:
    with pytest.raises(ValidationError) as excinfo:
        Settings()
    missing = {
        str(error["loc"][0])
        for error in excinfo.value.errors()
        if error["type"] == "missing"
    }
    assert missing == {
        "app_environment",
        "db_host",
        "db_port",
        "db_name",
        "db_username",
        "db_password",
    }


def test_settings_do_not_read_a_dotenv_file(
    tmp_path: Path, monkeypatch: MonkeyPatch, required_env: dict[str, str]
) -> None:
    (tmp_path / ".env").write_text("APP_NAME=from-file\nSERVER_PORT=19080\n")
    monkeypatch.chdir(tmp_path)
    settings = Settings()
    assert settings.app_name == "API"
    assert settings.server_port == 8000


def test_app_settings_are_independent(required_env: dict[str, str]) -> None:
    first = create_app(Settings(app_name="first", service_version="1"))
    second = create_app(Settings(app_name="second", service_version="2"))
    assert first.title == "first"
    assert second.title == "second"
    assert second.version == "2"


def _env_without_required() -> dict[str, str]:
    env = dict(os.environ)
    for key in REQUIRED_ENV:
        env.pop(key, None)
    return env


def test_missing_required_env_vars_exit_1_and_list_all_missing_keys() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "app.run"],
        cwd=os.getcwd(),
        env=_env_without_required(),
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 1
    assert "Missing or invalid environment variables:" in result.stderr
    for key in (
        "APP_ENVIRONMENT",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USERNAME",
        "DB_PASSWORD",
    ):
        assert key in result.stderr


def test_dotenv_file_in_cwd_is_not_read_by_the_process(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        "\n".join(f"{key}={value}" for key, value in REQUIRED_ENV.items())
    )
    result = subprocess.run(
        [sys.executable, "-m", "app.run"],
        cwd=tmp_path,
        env=_env_without_required(),
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    # A .env file sitting in cwd must not satisfy required vars — the process
    # only ever reads the real OS environment.
    assert result.returncode == 1
    assert "Missing or invalid environment variables:" in result.stderr


def test_invalid_environment_exits_without_leaking_input() -> None:
    secret = "synthetic-secret-value"
    result = subprocess.run(
        [sys.executable, "-m", "app.run"],
        cwd=os.getcwd(),
        env={**os.environ, **REQUIRED_ENV, "SERVER_PORT": secret},
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 1
    assert "Missing or invalid environment variables: SERVER_PORT" in result.stderr
    assert secret not in result.stderr + result.stdout
