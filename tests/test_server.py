"""Checks for the public liveness contract and local server startup."""

import pytest
from fastapi.testclient import TestClient

from youtube_sieve.__main__ import main
from youtube_sieve.config import ServerConfig
from youtube_sieve.transport.web import create_app


def test_health_returns_only_status():
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_default_config(monkeypatch):
    monkeypatch.delenv("YOUTUBE_SIEVE_HOST", raising=False)
    monkeypatch.delenv("YOUTUBE_SIEVE_PORT", raising=False)
    assert ServerConfig.from_env() == ServerConfig(host="127.0.0.1", port=8000)


@pytest.mark.parametrize(("host", "port"), [("0.0.0.0", "1"), ("::1", "65535")])
def test_config_overrides(monkeypatch, host, port):
    monkeypatch.setenv("YOUTUBE_SIEVE_HOST", host)
    monkeypatch.setenv("YOUTUBE_SIEVE_PORT", port)
    assert ServerConfig.from_env() == ServerConfig(host=host, port=int(port))


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("HOST", ""),
        ("HOST", "999.0.0.1"),
        ("PORT", ""),
        ("PORT", "abc"),
        ("PORT", "0"),
        ("PORT", "65536"),
    ],
)
def test_invalid_settings_stop_startup(monkeypatch, key, value):
    monkeypatch.setenv("YOUTUBE_SIEVE_HOST", "127.0.0.1")
    monkeypatch.setenv("YOUTUBE_SIEVE_PORT", "8000")
    monkeypatch.setenv(f"YOUTUBE_SIEVE_{key}", value)
    with pytest.raises(SystemExit, match=f"YOUTUBE_SIEVE_{key}"):
        main()
