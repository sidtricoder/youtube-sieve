"""Spike for #38: MCP SDK 2.3.0 mounted in FastAPI, Streamable HTTP, one public tool."""

import contextlib

from fastapi import FastAPI
from mcp.server import MCPServer

mcp = MCPServer("youtube-sieve-spike")


@mcp.tool()
def parse_duration(duration: str) -> dict:
    """Public tool: convert an ISO 8601 duration such as PT15M33S to seconds."""
    import re

    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not m:
        raise ValueError(f"not a duration: {duration!r}")
    h, mi, s = (int(x or 0) for x in m.groups())
    return {"seconds": h * 3600 + mi * 60 + s}


mcp_app = mcp.streamable_http_app(streamable_http_path="/mcp", stateless_http=True, json_response=True)


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.mount("/", mcp_app)
