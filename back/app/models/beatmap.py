from datetime import datetime
from pydantic import Field, BaseModel
from typing import Optional

'''
Models Optimized for AI Comprehension
'''


class AIBeatmapCovers(BaseModel):
    cover: str = Field(description="Beatmap cover image asset")
    card: str = Field(description="Beatmap card image asset")
    list: str = Field(description="Beatmap list image asset")
    slimcover: str = Field(description="Slim version of cover image asset")
    cover_2_x: Optional[str] = Field(default=None, alias="cover@2x")
    card_2_x: Optional[str] = Field(default=None, alias="card@2x")
    list_2_x: Optional[str] = Field(default=None, alias="list@2x")
    slimcover_2_x: Optional[str] = Field(default=None, alias="slimcover@2x")


class AIBeatmapHype(BaseModel):
    current: int = Field(description="Number of hypes the beatmap has")
    required: int = Field(description="Number of hypes necessary for ranked consideration")


class AIBeatmapGenre(BaseModel):
    name: str = Field(description="Genre of the song")
    id: int = Field(description="Id associated with the genre")


class AIBeatmapDescription(BaseModel):
    description: str = Field(description="Description of beatmap")


class AIBeatmapLanguage(BaseModel):
    name: str = Field(description="Name of the language")
    id: int = Field(description="Id associated with the language")


class AIBeatmap(BaseModel):
    id: int = Field(description="Unique id for beatmap")
    url: str = Field(description="Link to osu webpage for beatmap")
    mode: int = Field(
        description="Integer value denoting game mode for the beatmap; 0 = standard, 1 = taiko, 2 = Catch the Beat (CTB), 3 = Mania")
    beatmapset_id: int = Field(description="Unique id for beatmap set")
    difficulty_rating: float = Field(description="Difficulty star rating for beatmap")
    status: int = Field(
        description="Integer value denoting a beatmap set's status; -2 = Graveyard, -1 = WIP, 0 = Pending, 1 = Ranked, 2 = Approved, 3 = Qualified, 4 = Loved")
    total_length: int = Field(description="The length of the song in seconds")
    user_id: int = Field(description="User id of the mapper")
    version: str = Field(description="Name of the beatmap difficulty")
    accuracy: Optional[float] = Field(
        description="Number indicating how accurate timing needs to be; 0 = least accurate, 10+ = most accurate")
    ar: Optional[float] = Field(
        description="Number indicating how long you have to react to the circle appearing on screen before it disappears; 0 = slowest, 10+ = fastest")
    cs: Optional[float] = Field(description="Number indicating how big the circles are; 0 = Biggest, 10+ = smallest")
    bpm: Optional[float] = Field(description="song beats per minute")
    convert: Optional[bool] = Field(description="Whether a beatmap is a convert")
    count_circles: Optional[int] = Field(description="How many circles are in the beatmap")
    count_sliders: Optional[int] = Field(description="How many sliders are in the beatmap")
    count_spinners: Optional[int] = Field(description="How many spinners are in the beatmap")
    drain: Optional[float] = Field(
        description="Number indicating how fast health will drain; 0 = slowest, 10+ = fastest")
    hit_length: Optional[int] = Field(description="The length of active playtime in seconds")
    is_scoreable: Optional[bool] = Field(description="Whether or not scores can be submitted on the beatmap")
    last_updated: Optional[datetime] = Field(description="Last time the beatmap set was updated")
    passcount: Optional[int] = Field(description="Number of times the map has been passed (non-unique")
    play_count: Optional[int] = Field(alias="playcount",
                                      description="Number of times the map has been played (non-unique)")
    max_combo: Optional[int] = Field(description="Maximum combo possible")


class AIBeatmapset(BaseModel):
    id: int = Field(description="Unique id for beatmap set")
    artist: str = Field(description="Song artist name (romanized)")
    artist_unicode: str = Field(description="Song artist name in orignal language")
    covers: AIBeatmapCovers = Field(description="Information for the cover image of a beatmap set")
    creator: str = Field(description="Username of the beatmap set's creator")
    favourite_count: int = Field(description="Number of favorites the map has")
    play_count: int = Field(alias="playcount", description="Number of times the map has been played (non-unique)")
    preview_url: str = Field(description="Song preview url (leads to audio file)")
    source: str = Field(description="The song's source material for example, if the song came from a game")
    status: int = Field(
        description="integer value denoting a beatmap set's status; -2 = Graveyard, -1 = WIP, 0 = Pending, 1 = Ranked, 2 = Approved, 3 = Qualified, 4 = Loved")
    title: str = Field(description="Song title (romanized_")
    title_unicode: str = Field(description="Song title in original language")
    user_id: int = Field(description="User id of the mapper")
    video: bool = Field(description="Tells whether there is a video")
    nsfw: Optional[bool] = Field(description="Tells if the content is NSFW")
    hype: Optional[AIBeatmapHype] = Field(
        description="Information on a beatmap set's hype status (related to ranking process")
    bpm: Optional[float] = Field(description="Song beats per minute")
    is_scoreable: Optional[bool] = Field(description="Whether scores can be submitted on the beatmap set")
    last_updated: Optional[datetime] = Field(description="Last time the beatmap set was updated")
    ranked_date: Optional[datetime] = Field(description="When the beatmap set was ranked")
    storyboard: Optional[bool] = Field(description="If the map has a storyboard")
    submitted_date: Optional[datetime] = Field(description="When the beatmap set was submitted")
    tags: Optional[str] = Field(description="Descriptive tags of beatmap set and song attributes")
    description: Optional[AIBeatmapDescription] = Field(description="Beatmap set description")
    genre: Optional[AIBeatmapGenre] = Field(description="Genre of the song")
    language: Optional[AIBeatmapLanguage] = Field(description="Language of the song")
    beatmaps: Optional[list[AIBeatmap]] = Field(description="Beatmaps belonging to the set")
    converts: Optional[list[AIBeatmap]] = Field(
        description="Beatmaps converted to other game modes automatically (not the best don't recommend as first choice)")


class AIBeatmapsetSearchResponse(BaseModel):
    beatmapsets: list[AIBeatmapset] = Field(description="List of beatmap sets")
