# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel
from openai import AsyncOpenAI
from ...config import Config
from agents import Agent, OpenAIChatCompletionsModel
from ..tools.chart_tool import ChartRequest

external_client = AsyncOpenAI(
    base_url=Config.EXTERNAL_API_BASE_URL,
    api_key=Config.EXTERNAL_API_KEY,
)

PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words.\n\n"
    "Important: When writing the report, you should:\n"
    "1. Include data visualizations (charts) where appropriate:\n"
    "   - Add a placeholder like {{chart_1}}, {{chart_2}} etc. in the markdown_report\n"
    "   - Add an entry to the charts list with chart data in Markdown table format, for example:\n"
    "     | Category | Value | Description |\n"
    "     |----------|--------|-------------|\n"
    "     | Item 1   | 100    | Detail 1    |\n"
    "     | Item 2   | 200    | Detail 2    |\n"
    "   - Each chart request should include:\n"
    "     * Chart type (bar, line, pie, etc.)\n"
    "     * Chart title\n"
    "     * Data in Markdown table format\n"
    "     * A brief description of what the chart should show\n"
    "     * The position marker (e.g., chart_1) matching the placeholder\n"
    "2. Make sure the report flows naturally with text and charts integrated together."
)
MODEL_NAME = "o3-mini"


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""

    chart_requests: list[ChartRequest]
    """List of requested charts and their placement information"""


writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=external_client),
    output_type=ReportData,
)
