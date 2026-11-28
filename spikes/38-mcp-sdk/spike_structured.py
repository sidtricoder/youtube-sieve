import asyncio
from pydantic import BaseModel
from mcp import Client
from mcp.server import MCPServer

mcp = MCPServer("s")

class Seconds(BaseModel):
    seconds: int

@mcp.tool()
def to_seconds(minutes: int) -> Seconds:
    """Typed output."""
    return Seconds(seconds=minutes * 60)

async def main():
    async with Client(mcp) as c:   # in-process: SDK supports this for tests
        t = (await c.list_tools()).tools[0]
        print("outputSchema:", t.output_schema)
        r = await c.call_tool("to_seconds", {"minutes": 2})
        print("structured:", r.structured_content, "| is_error:", r.is_error)
        bad = await c.call_tool("to_seconds", {"minutes": "x"})
        print("invalid input -> is_error:", bad.is_error)
asyncio.run(main())
