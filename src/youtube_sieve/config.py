"""Read and validate the local server's environment at startup."""

from __future__ import annotations

import os
from dataclasses import dataclass
from ipaddress import ip_address


@dataclass(frozen=True)
class ServerConfig:
    host: str
    port: int

    @classmethod
    def from_env(cls) -> ServerConfig:
        host = os.environ.get("YOUTUBE_SIEVE_HOST", "127.0.0.1")
        try:
            ip_address(host)
        except ValueError as exc:
            raise ValueError("YOUTUBE_SIEVE_HOST must be an IPv4 or IPv6 address") from exc

        raw_port = os.environ.get("YOUTUBE_SIEVE_PORT", "8000")
        if not (raw_port.isascii() and raw_port.isdecimal() and len(raw_port) <= 5):
            raise ValueError("YOUTUBE_SIEVE_PORT must be a decimal port from 1 to 65535")
        port = int(raw_port)
        if not 1 <= port <= 65535:
            raise ValueError("YOUTUBE_SIEVE_PORT must be a decimal port from 1 to 65535")
        return cls(host=host, port=port)
