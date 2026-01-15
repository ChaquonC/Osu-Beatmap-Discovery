from typing import Any


def ok(data: dict):
    return {
        "ok": True,
        "data": data,
    }


def fail(code: int, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message
        }
    }
