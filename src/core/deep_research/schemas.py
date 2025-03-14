from pydantic import BaseModel


class DeepResearchRequest(BaseModel):
    query: str


class DeepResearchResponse(BaseModel):
    trace_id: str
    report: str
    summary: str
    follow_up_questions: list[str]
