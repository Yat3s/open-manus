from pydantic import BaseModel

from agents import Agent
from datetime import datetime

from core.deep_research.model import PlannerModel

search_task_count = 20

current_time = datetime.now().strftime("%Y/%m/%d")
PROMPT = (
    """
Task Instructions:
You are an experienced research analyst responsible for defining the search keywords and information-gathering strategy to prepare an in-depth investment research report on company. Based on the report framework and requirements below, please design ${search_task_count} precise search keywords, key data indicators, and information sources to ensure that the subsequent search agent can efficiently collect the latest relevant data and materials.
current date is ${current_time}
Report Framework and Requirements:
Company background and management analysis
Analysis of the company’s core business
Analysis of the current competitive landscape and industry situation
Financial revenue analysis (including revenue growth and profit margins)

Information Sources to Consider:
Company official website
Annual reports and financial statements from previous years
Reviews on Glassdoor and LinkedIn
Industry analysis reports (e.g., Gartner, etc.)
Other public sources

General Tips:
Target data should be as current as possible, with a cutoff date of ${current_time}.
Ensure that the search keywords cover multiple dimensions of information (management, business, competition, finance, etc.).
Clearly list the suggested keywords or search directions for each section to support comprehensive data collection."""
)

class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="Planner Agent",
    instructions=PROMPT,
    model=PlannerModel.get_model(),
    output_type=WebSearchPlan,
)
