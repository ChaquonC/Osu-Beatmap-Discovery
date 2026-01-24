import pytest
import pytest_asyncio

from app.core.llm_logic import agent_levels


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "agent_code, expected",
    [
        ("thinking_on_a_budget", 1),
        ("basic", 2),
        ("hes_cooking", 3),
        ("the_thinker", 4),
    ],
)
def test_agent_levels_valid_codes(agent_code, expected):
    assert agent_levels(agent_code) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bad_code",
    [
        "unknown",
        "Thinking_On_A_Budget",
        "",
        " basic ",
    ],
)
def test_agent_levels_invalid_string_raises_keyerror(bad_code):
    with pytest.raises(KeyError):
        agent_levels(bad_code)