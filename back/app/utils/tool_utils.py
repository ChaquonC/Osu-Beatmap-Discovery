from typing import Any

from app.utils import InvalidRequest


def ok(data: dict = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
    if "ok" in data or "ok" in kwargs:
        raise InvalidRequest("Assigning variable to reserved key")
    return {"content": {"type": "json", "json": {"ok": True, **(data or {}), **kwargs}}}


def fail(code: int, message: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
    if "ok" in kwargs:
        raise InvalidRequest("Assigning variable to reserved key")
    return {"content": {"type": "json", "json": {"ok": False, "code": code, "message": message, **kwargs}}}
