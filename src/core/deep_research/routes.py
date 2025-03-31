from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.deep_research.manager import DeepResearchManager
from core.deep_research.schemas import DeepResearchRequest, DeepResearchResponse

deep_research_router = APIRouter()


@deep_research_router.post("/deep_research", response_model=DeepResearchResponse)
async def create_deep_research(
    request: DeepResearchRequest,
) -> DeepResearchResponse:
    manager = DeepResearchManager()
    result = await manager.run(request.query)
    return result


@deep_research_router.post("/deep_research_stream")
async def create_deep_research_stream(
    request: DeepResearchRequest,
) -> StreamingResponse:
    manager = DeepResearchManager()
    return StreamingResponse(
        manager.run_stream(request.query), media_type="text/event-stream"
    )
