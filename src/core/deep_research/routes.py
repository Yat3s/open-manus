from fastapi import APIRouter
from core.deep_research.manager import DeepResearchManager
from core.deep_research.schemas import DeepResearchRequest, DeepResearchResponse

deep_research_router = APIRouter()


@deep_research_router.post("/deep_research", response_model=DeepResearchResponse)
async def create_deep_research(request: DeepResearchRequest) -> DeepResearchResponse:
    manager = DeepResearchManager()
    result = await manager.run(request.query)
    return result
