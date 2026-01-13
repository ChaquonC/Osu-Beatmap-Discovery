import pytest
import pytest_asyncio

from typing import Any

from app.utils import InvalidRequest
from app.utils.tool_utils import ok, fail


def is_subdict(small: dict, big: dict) -> bool:
    return all(k in big and big[k] == v for k, v in small.items())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data,kwargs",
    [
        ({1: 2}, {}),
        ({1: "fdfd"}, {"all": "crave"}),
        ({"shark": "tank"}, {}),
        ({(1, 2): "play"}, {"a": 1}),
        ({}, {"a": 1, "b": 2}),
        ({"a": 1, "b": 2}, {"a": 1, "b": 2, "c": 3, "d": [], "e": "blah"}),
        ({"data": "totally_real_data"}, {"number": 10000000000})
    ]
)
async def test_ok(data: dict, kwargs: dict[str, Any]):
    response = ok(data=data, **kwargs)
    assert isinstance(response["content"], dict)
    assert response["content"]["type"] == "json"
    assert isinstance(response["content"]["json"], dict)
    assert response["content"]["json"]["ok"] == True
    json = response["content"]["json"]
    assert len(json) >= 2
    if data is not None:
        assert is_subdict(data, json)
    assert is_subdict(kwargs, json)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data,kwargs",
    [
        ({"ok": 2}, {"totally_real_data": "real_data"}),
        ({"totally_real_data": "real_data"}, {"ok": "we_ok"}),
        ({"ok": 1}, {"ok": 2})
    ]
)
async def test_ok_error(data: dict, kwargs: dict[str, Any]):
    with pytest.raises(InvalidRequest):
        ok(data=data, **kwargs)

def test_fail_basic_shape():
    resp = fail(400, "bad request")

    assert resp["content"]["type"] == "json"
    payload = resp["content"]["json"]

    assert payload["ok"] is False
    assert payload["code"] == 400
    assert payload["message"] == "bad request"


def test_fail_includes_extra_fields():
    resp = fail(404, "not found", resource="user", user_id=123)

    payload = resp["content"]["json"]
    assert payload["ok"] is False
    assert payload["code"] == 404
    assert payload["message"] == "not found"
    assert payload["resource"] == "user"
    assert payload["user_id"] == 123


def test_fail_rejects_reserved_ok_key():
    with pytest.raises(InvalidRequest, match="reserved key"):
        fail(500, "server error", ok=True)


@pytest.mark.parametrize(
    "bad_ok_value",
    [True, False, 1, "yes", None, {"x": 1}],
)
def test_fail_rejects_reserved_ok_key_any_value(bad_ok_value: Any):
    with pytest.raises(InvalidRequest):
        fail(400, "bad", ok=bad_ok_value)