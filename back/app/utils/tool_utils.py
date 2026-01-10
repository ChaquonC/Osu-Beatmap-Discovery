from typing import Any


def ok(data: dict = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
    return {"content": {"type": "json", "json": {"ok": True, **(data or {}), **kwargs}}}


def fail(code: int, message: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
    return {"content": {"type": "json", "json": {"ok": False, "code": code, "message": message, **kwargs}}}
