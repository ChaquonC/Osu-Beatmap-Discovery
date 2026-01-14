import pytest
import pytest_asyncio

from unittest.mock import MagicMock, AsyncMock

import app.tools.beatmap_search


@pytest.fixture
def mod():
    return app.tools.beatmap_search


@pytest.fixture
def fake_client():
    client = MagicMock()
    client.search_beatmapsets = AsyncMock()
    client.aclose = AsyncMock()
    return client


class FakeResponse:
    """Mimics the object returned by client.search_beatmapsets(...)"""
    def __init__(self, raw_payload: dict):
        self._raw_payload = raw_payload
        self.model_dump_calls = []

    def model_dump(self, *args, **kwargs):
        self.model_dump_calls.append((args, kwargs))
        return self._raw_payload


@pytest.mark.asyncio
async def test_beatmap_search_success_calls_client_with_normalized_params(mod, fake_client, monkeypatch):
    monkeypatch.setattr(mod, "osu_client", fake_client)

    fake_resp = FakeResponse(raw_payload={"beatmapsets": []})
    fake_client.search_beatmapsets.return_value = fake_resp

    sentinel = object()
    monkeypatch.setattr(
        mod.AIBeatmapsetSearchResponse,
        "model_validate",
        staticmethod(lambda raw: sentinel),
    )

    search = mod.BeatmapSearchQuery(
        query="camellia",
        mode=None,
        category="ranked",
        only_video=False,
    )

    result = await mod.beatmap_search(search)
    assert result is sentinel

    fake_client.search_beatmapsets.assert_awaited_once()
    passed_kwargs = fake_client.search_beatmapsets.await_args.kwargs

    assert passed_kwargs["query"] == "camellia"
    assert passed_kwargs["category"] == "ranked"
    assert passed_kwargs["only_video"] is False
    assert "mode" not in passed_kwargs  # exclude_none=True behavior

    # Ensure response.model_dump called with expected settings
    assert len(fake_resp.model_dump_calls) == 1
    _, dump_kwargs = fake_resp.model_dump_calls[0]
    assert dump_kwargs == {"mode": "json", "by_alias": True}


@pytest.mark.asyncio
async def test_beatmap_search_empty_query_raises_toolerror(mod, fake_client, monkeypatch):
    monkeypatch.setattr(mod, "osu_client", fake_client)

    # query is required by model, but empty string is still a valid str => hits your guard
    search = mod.BeatmapSearchQuery(query="")

    with pytest.raises(mod.ToolError) as exc:
        await mod.beatmap_search(search)

    assert str(exc.value) == "Search must include 'query'"
    fake_client.search_beatmapsets.assert_not_called()


@pytest.mark.asyncio
async def test_beatmap_search_api_exception_maps_to_toolerror(mod, fake_client, monkeypatch):
    monkeypatch.setattr(mod, "osu_client", fake_client)

    fake_client.search_beatmapsets.side_effect = mod.APIException("nope")
    search = mod.BeatmapSearchQuery(query="anything")

    with pytest.raises(mod.ToolError) as exc:
        await mod.beatmap_search(search)

    assert str(exc.value) == "api call failed"


@pytest.mark.asyncio
async def test_beatmap_search_refresh_token_expired_maps_to_toolerror(mod, fake_client, monkeypatch):
    monkeypatch.setattr(mod, "osu_client", fake_client)

    fake_client.search_beatmapsets.side_effect = mod.RefreshTokenExpiredError("expired")
    search = mod.BeatmapSearchQuery(query="anything")

    with pytest.raises(mod.ToolError) as exc:
        await mod.beatmap_search(search)

    assert str(exc.value) == "expired api token could not be refreshed"


@pytest.mark.asyncio
async def test_beatmap_search_unexpected_exception_message_becomes_toolerror_message(mod, fake_client, monkeypatch):
    monkeypatch.setattr(mod, "osu_client", fake_client)

    fake_client.search_beatmapsets.side_effect = RuntimeError("boom")
    search = mod.BeatmapSearchQuery(query="anything")

    with pytest.raises(mod.ToolError) as exc:
        await mod.beatmap_search(search)

    assert str(exc.value) == "boom"