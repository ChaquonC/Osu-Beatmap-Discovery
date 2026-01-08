from typing import Any


def ok(data: Any = None, **kwargs: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "json", "json": {"ok": True, **(data or {}), **kwargs}}]}


def fail(code: int, message: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
    return {"content": [{"type": "json", "json": {"ok": False, "code": code, "message": message, **kwargs}}]}


class ToolError(Exception):
    def __init__(self, code=500, message="Tool failed", data=None):
        super().__init__(message)
        self.code, self.data = code, data or {}