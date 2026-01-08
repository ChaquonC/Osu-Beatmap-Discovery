from pydantic import BaseModel, Field
from typing import Optional
from aiosu.models import Gamemode


class BeatmapLookupQuery(BaseModel):
    query: Optional[str] = Field(description="Search query")
    mode: Gamemode = Field(
        description="Integer value denoting game mode for the beatmap; 0 = standard, 1 = taiko, 2 = Catch the Beat (CTB), 3 = Mania")