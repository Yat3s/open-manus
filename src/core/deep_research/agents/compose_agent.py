# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel
from agents import Agent
from ..tools.chart_tool import ChartRequest
from ..model import ComposeModel
from datetime import datetime

current_time = datetime.now().strftime("%Y/%m/%d")
PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "Current time: {current_time}\n"
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

# PROMPT = (
# """
# Task Instructions:
# You are a senior secondary market buy-side analyst tasked with drafting an in-depth, rigorously structured investment research report on company based on all collected public information and data.
# Overall Report Framework and Content Requirements:
# Analysis of Company Background and Management
# Analysis of the Company's Core Business
# Analysis of the Current Competitive Landscape and Industry Situation
# Analysis of the Company's Financial Revenue (including revenue growth and profit margins)

# General Tips:
# The report should be logically clear and data-rich, providing strong support for investment decision-making (for reference and learning purposes only, and not to be construed as investment advice).
# All data, figures, and interview references must clearly indicate their specific public sources.
# Employ rigorous data analysis methods and logical reasoning throughout the report drafting process. If estimations are necessary, please specify the estimation methods and the related uncertainties.
# To enhance readability, use tables and charts as much as possible to present the data.
# """
# )

class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report"""
    
    follow_up_questions: list[str]
    """Suggested topics to research further"""

    chart_requests: list[ChartRequest]
    """List of requested charts and their placement information"""


compose_agent = Agent(
    name="Compose Agent",
    instructions=PROMPT,
    model=ComposeModel.get_model(),
    output_type=ReportData,
)
