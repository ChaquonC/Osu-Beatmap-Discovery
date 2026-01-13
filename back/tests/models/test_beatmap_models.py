import pytest
import pytest_asyncio

from app.models import AIBeatmapCovers, AIBeatmap, AIBeatmapset

@pytest.mark.asyncio
async def test_covers_alias_fields_parse():
    covers = AIBeatmapCovers.model_validate({
        "cover": "a",
        "card": "b",
        "list": "c",
        "slimcover": "d",
        "cover@2x": "aa",
        "card@2x": "bb",
    })
    assert covers.cover_2_x == "aa"
    assert covers.card_2_x == "bb"

@pytest.mark.asyncio
async def test_playcount_alias_parses():
    bm = AIBeatmap.model_validate({
        "id": 1,
        "url": "u",
        "mode": 0,
        "beatmapset_id": 10,
        "difficulty_rating": 5.0,
        "status": 1,
        "total_length": 123,
        "user_id": 9,
        "version": "Hard",
        "playcount": 777,
    })
    assert bm.play_count == 777

    bms = AIBeatmapset.model_validate({
        "id": 10,
        "artist": "a",
        "artist_unicode": "a",
        "covers": {"cover":"a","card":"b","list":"c","slimcover":"d"},
        "creator": "me",
        "favourite_count": 1,
        "playcount": 888,
        "preview_url": "p",
        "source": "s",
        "status": 1,
        "title": "t",
        "title_unicode": "t",
        "user_id": 9,
        "video": False,
    })
    assert bms.play_count == 888

