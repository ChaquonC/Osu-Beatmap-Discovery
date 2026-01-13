from typing import Any
from app.utils import InvalidRequest
from app.models import Tool
from fastmcp import FastMCP


def ok(data: dict = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
    if "ok" in data or "ok" in kwargs:
        raise InvalidRequest("Assigning variable to reserved key")
    return {"content": {"type": "json", "json": {"ok": True, **(data or {}), **kwargs}}}


def fail(code: int, message: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
    if "ok" in kwargs:
        raise InvalidRequest("Assigning variable to reserved key")
    return {"content": {"type": "json", "json": {"ok": False, "code": code, "message": message, **kwargs}}}


def register_tools(tools: list[Tool], mcp: FastMCP):
    for tool in tools:
        mcp.tool(
            name=tool.name,
            description=tool.description,
            tags=tool.tags,
            meta=tool.metadata
        )(tool.fn)