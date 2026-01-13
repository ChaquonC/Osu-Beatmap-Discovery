from app.models import Tool
from .beatmap_search import beatmap_search_tool

tools = [
    Tool(
        fn=beatmap_search_tool,
        name="Beatmap_Search",
        description="Returns a list of beatmap sets resulting from query and filters",
        tags={"beatmap", "search"},
        metadata={"version": 1.0}
    )
]
