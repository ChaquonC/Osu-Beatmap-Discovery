from pydantic import BaseModel, Field
from typing import Optional

"""
Query models for API based tools
"""


class BeatmapSearchQuery(BaseModel):
    query: str = Field(description="Search query")
    mode: Optional[int] = Field(
        default=None,
        description="Integer value denoting game mode for the beatmap; 0 = standard, 1 = taiko, 2 = Catch the Beat (CTB), 3 = Mania")
    category: Optional[str] = Field(
        default=None,
        description="beatmap category; can be: leaderboard, ranked, qualified, loved, favourites, pending, wip, graveyard and mine")
    show_explicit: Optional[bool] = Field(
        default=True,
        description="Whether or not to show explicit songs, defaults to True")
    genre: Optional[int] = Field(
        default=None,
        description="Integer value denoting song genre; 1 = Unspecified, 2 = Video game, 3 = Anime, 4 = Rock, 5 = Pop, 6 = Other, 7 = Novelty, 9 = Hip hop, 10 = Electronic, 11 = Metal, 12 = Classical, 13 = Folk, 14 = Jazz")
    language: Optional[int] = Field(
        default=None,
        description="Integer value denoting song language; 1 = Unspecified, 2 = English, 3 = Japanese, 4 = Chinese, 5 = Instrumental, 6 = Korean, 7 = French, 8 = German, 9 = Swedish, 10 = Spanish, 11 = Italian, 12 = Russian, 13 = Polish, 14 = Other")
    sort: Optional[str] = Field(
        default=None,
        description="How the information will be received; Options: title_asc, title_desc, artist_asc, artist_desc, difficulty_asc, difficulty_desc, ranked_asc, ranked_desc, rating_asc, rating_desc, plays_asc, plays_desc, favourites_asc, favourites_desc")
    only_video: Optional[bool] = Field(
        default=False,
        description="Whether to only include beatmaps sets that include video, defaults to False")
    only_storyboard: Optional[bool] = Field(
        default=False,
        description="Whether to only include beatmap sets that include storyboards, defaults to False")
    only_featured_artists: Optional[bool] = Field(
        default=False,
        description="Whether to only include beatmap sets with only featured artists, defaults to False")
