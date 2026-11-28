"""Call the spike server with the SDK's own client over real HTTP."""

import asyncio
import json

import httpx2
from mcp import Client

URL = "http://127.0.0.1:8765"


async def main() -> None:
    print("health:", httpx2.get(URL + "/health").json())
    async with Client(URL + "/mcp") as client:
        tools = await client.list_tools()
        print("tools:", [t.name for t in tools.tools])
        ok = await client.call_tool("parse_duration", {"duration": "PT15M33S"})
        print("call ok: isError=", ok.is_error, "structured=", ok.structured_content)
        bad = await client.call_tool("parse_duration", {"duration": "nonsense"})
        print("call bad: isError=", bad.is_error, "text=", bad.content[0].text[:80])
    # Raw 2026-07-28 request: no initialize handshake, version and capabilities in _meta
    body = {"jsonrpc": "2.0", "id": 1, "method": "tools/list",
            "params": {"_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28",
                                 "io.modelcontextprotocol/clientCapabilities": {}}}}
    r = httpx2.post(URL + "/mcp", json=body, headers={
        "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": "tools/list"})
    print("stateless raw tools/list:", r.status_code, json.dumps(r.json())[:160])


asyncio.run(main())
