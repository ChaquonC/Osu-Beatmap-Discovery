from fastmcp import FastMCP
from app.models.query import BeatmapSearchQuery
from app.tools.beatmap_search import beatmap_search
from app.utils.exceptions import InvalidRequest, ToolError
from app.utils.tool_utils import ok, fail

mcp = FastMCP(name="Beatmap-Discovery-Tools")

@mcp.tool(
    name="Beatmap_Search",
    description="Returns a list of beatmap sets resulting from query and filters",
    tags={"beatmap", "search"},
    meta={"version": 1.0}
)
async def beatmap_search_tool(search: BeatmapSearchQuery) -> dict:
    try:

        result = await beatmap_search(search)
        raw_data = result.model_dump(mode="json", by_alias=True, exclude_none=True)

        if len(raw_data) == 0:
            return fail(code=404, message="Search resulted in no beatmap sets returned")

        return ok(raw_data)
    except InvalidRequest as e:
        return fail(code=500, message=f"Invalid Request: {str(e)}")
    except ToolError as e:
        return fail(code=e.code, message=str(e), data=e.data)

mcp_app = mcp.http_app()
