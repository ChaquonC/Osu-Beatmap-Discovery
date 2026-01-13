import pytest
import pytest_asyncio

from app.utils.exceptions import ToolError

def test_toolerror_defaults():
    err = ToolError()

    assert isinstance(err, Exception)
    assert str(err) == "Tool failed"
    assert err.code == 500
    assert err.data == {}


def test_toolerror_custom_message_only():
    err = ToolError(message="Nope")

    assert str(err) == "Nope"
    assert err.code == 500
    assert err.data == {}


def test_toolerror_custom_code_message_and_data():
    err = ToolError(code=404, message="Not found", data={"id": 123})

    assert str(err) == "Not found"
    assert err.code == 404
    assert err.data == {"id": 123}


def test_toolerror_data_none_becomes_empty_dict():
    err = ToolError(data=None)
    assert err.data == {}


def test_toolerror_data_is_not_shared_between_instances():
    a = ToolError()
    b = ToolError()

    a.data["x"] = 1
    assert b.data == {}  # make sure no accidental shared mutable default


def test_toolerror_raises_and_is_catchable():
    with pytest.raises(ToolError) as exc_info:
        raise ToolError(code=400, message="Bad input", data={"field": "name"})

    err = exc_info.value
    assert str(err) == "Bad input"
    assert err.code == 400
    assert err.data == {"field": "name"}