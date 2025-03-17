# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research "
    "assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words.\n\n"
    "Important: When writing the report, you should:\n"
    "1. Include relevant images by searching for them using search terms related to your content.\n"
    "2. For each image you want to include:\n"
    "   - Add a placeholder like {{image_1}}, {{image_2}} etc. in the markdown_report where you want the image to appear\n"
    "   - Add an entry to the images list with:\n"
    "     * A search query to find a relevant image\n"
    "     * A descriptive caption for the image\n"
    "     * The position marker matching the placeholder\n"
    "3. Make sure the report flows naturally with text and images integrated together."
)


class ImageRequest(BaseModel):
    search_query: str
    """The search query to find this image"""

    caption: str
    """Caption to display under the image"""

    position: str
    """Where to place the image in the report (e.g. {{image_1}})"""


class ReportData(BaseModel):
    short_summary: str
    """A short 2-3 sentence summary of the findings."""

    markdown_report: str
    """The final report with image placeholders"""

    follow_up_questions: list[str]
    """Suggested topics to research further"""

    image_requests: list[ImageRequest]
    """List of requested images and their placement information"""


writer_agent = Agent(
    name="WriterAgent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=ReportData,
)
