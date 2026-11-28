# Spike #38: MCP Python SDK, FastAPI and HTTP client

**Throwaway code. This branch is never merged.** Findings are recorded in `brain/areas/decision-tech-stack.md` and ADR 0004.

Versions tried (Python 3.12): `mcp==2.3.0`, `fastapi==0.165.0`, `uvicorn==0.54.0`, `httpx2==2.16.2` (an `mcp` dependency), `respx==0.23.1`.

## Files
- `spike_server.py`: `MCPServer` with one public tool, its Streamable HTTP app (`stateless_http=True`, `json_response=True`) mounted in FastAPI next to `GET /health`, with the SDK session manager run in the FastAPI lifespan.
- `spike_client.py`: the SDK `Client` over real HTTP (list and call tools, including a failing call), then a raw 2026-07-28 request with no `initialize`.
- `spike_structured.py`: a typed Pydantic return value, and the in-process `Client(server)` for tests.

## Run
```bash
pip install mcp==2.3.0 fastapi==0.165.0 uvicorn==0.54.0
uvicorn --app-dir spikes/38-mcp-sdk spike_server:app --port 8765 &
python spikes/38-mcp-sdk/spike_client.py
python spikes/38-mcp-sdk/spike_structured.py
```

## Observed results
| Check | Result |
|---|---|
| `mcp_types.LATEST_PROTOCOL_VERSION` | `2026-07-28`; the SDK also serves the older `initialize`-based revisions |
| `/health` and `/mcp` in one FastAPI app | works; the SDK session manager must run inside the FastAPI lifespan |
| SDK client: list and call a tool | works |
| Tool raises an exception | returned as a result with `is_error=True`, not a protocol error |
| Raw `tools/list` with only `_meta` protocolVersion and capabilities, no `initialize` | HTTP 200 with the tool list (stateless 2026-07-28 works) |
| Typed Pydantic return value | tool gets an `outputSchema` and returns `structured_content` |
| Wrong argument type | rejected by schema validation before the tool runs, `is_error=True` |
| In-process `Client(server)` | works, so tool tests need no network |
| SDK 2.x result attributes | snake_case: `is_error`, `structured_content`, `output_schema` |
| Authorization server, server side | Protected Resource Metadata, 401 challenge, token verifier, authorize/token/register/revoke routes built in; **Client ID Metadata Documents: client side only**, no server-side fetching, and the generated metadata does not advertise them |
| `httpx2.MockTransport` | works, injected through the client constructor |
| **RESPX with `httpx2`** | **does not intercept**: the "mocked" request went to the real network (stopped only by the sandbox proxy) |
