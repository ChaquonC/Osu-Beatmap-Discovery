import pytest
import pytest_asyncio

from app.utils.tool_utils import ok, fail


def test_ok_with_simple_dict():
    data = {"a": 1, "b": "test"}

    result = ok(data)

    assert result == {
        "ok": True,
        "data": data,
    }


def test_ok_with_empty_dict():
    data = {}

    result = ok(data)

    assert result["ok"] is True
    assert result["data"] == {}


def test_ok_preserves_nested_data():
    data = {
        "items": [
            {"id": 1},
            {"id": 2}
        ],
        "meta": {"count": 2}
    }

    result = ok(data)

    assert result["data"]["items"][0]["id"] == 1
    assert result["data"]["meta"]["count"] == 2


def test_fail_basic_error():
    result = fail(400, "Bad request")

    assert result == {
        "ok": False,
        "error": {
            "code": 400,
            "message": "Bad request",
        }
    }


def test_fail_with_different_code():
    result = fail(500, "Internal error")

    assert result["ok"] is False
    assert result["error"]["code"] == 500
    assert result["error"]["message"] == "Internal error"


def test_fail_message_is_string():
    message = "Something went wrong"
    result = fail(404, message)

    assert isinstance(result["error"]["message"], str)