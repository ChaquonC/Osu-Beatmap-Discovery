import pytest
import pytest_asyncio

from typing import Any
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
        (None, {"a": 1}),
        ({"data": "totally_real_data"}, {"number": 10000000000})
    ]
)
async def test_ok_success(data: dict, kwargs: dict[str, Any]):
    response = ok(data, **kwargs)
    assert isinstance(response["content"], dict)
    assert response["content"]["type"] == "json"
    assert isinstance(response["content"]["json"], dict)
    assert response["content"]["json"]["ok"] == True
    json = response["content"]["json"]
    assert len(json) >= 2
    if data is not None:
        assert is_subdict(data, json)
    assert is_subdict(kwargs, json)

