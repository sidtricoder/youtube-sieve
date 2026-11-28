"""Start the web transport with python -m youtube_sieve."""

import uvicorn

from youtube_sieve.config import ServerConfig
from youtube_sieve.transport.web import create_app


def main() -> None:
    try:
        config = ServerConfig.from_env()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    uvicorn.run(create_app(), host=config.host, port=config.port)


if __name__ == "__main__":
    main()
