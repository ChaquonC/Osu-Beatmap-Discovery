from app.models import ToolRegistry, Tool
from .beatmap_search import BeatmapSearchQuery, beatmap_search_tool

tool_registry = ToolRegistry(
    tools={
        "beatmap_search": Tool(
            name="beatmap_search",
            description="gives list of beatmap sets given query",
            fn=beatmap_search_tool,
            input_model=BeatmapSearchQuery
        )
    }
)
