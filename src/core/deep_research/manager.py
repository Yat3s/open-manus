from __future__ import annotations

import asyncio
import logging

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace

from .agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from .agents.search_agent import search_agent
from .agents.writer_agent import ReportData, writer_agent
from .tools.chart_tool import ChartRequest, generate_chart
from .printer import Printer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("deep_research_manager")


class DeepResearchManager:
    def __init__(self):
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, query: str) -> dict:
        trace_id = gen_trace_id()
        logger.info(f"Starting research with trace_id: {trace_id}")
        logger.info(f"Query: {query}")

        with trace("Research trace", trace_id=trace_id):
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            report = await self._write_report(query, search_results)

            logger.info(
                f"Report generated with {len(report.chart_requests)} chart requests"
            )
            for i, chart in enumerate(report.chart_requests):
                logger.info(
                    f"Chart {i+1}: {chart.title} (Type: {chart.chart_type}, Position: {chart.position})"
                )

            processed_report = report.markdown_report

            # Process chart requests
            for i, chart_request in enumerate(report.chart_requests):
                logger.info(
                    f"Processing chart request {i+1}/{len(report.chart_requests)}: {chart_request.title}"
                )
                chart_url = await self._generate_chart(chart_request)
                markdown_chart = f"\n![{chart_request.title}]({chart_url})\n"
                placeholder = f"{{{{{chart_request.position}}}}}"

                if placeholder in processed_report:
                    logger.info(f"Replacing placeholder {placeholder} with chart image")
                    processed_report = processed_report.replace(
                        placeholder, markdown_chart
                    )
                else:
                    logger.warning(f"Placeholder {placeholder} not found in report")

            logger.info("Research completed successfully")
            return {
                "trace_id": trace_id,
                "report": processed_report,
                "summary": report.short_summary,
                "follow_up_questions": report.follow_up_questions,
            }

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        logger.info("Planning searches")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        plan = result.final_output_as(WebSearchPlan)
        logger.info(f"Search plan created with {len(plan.searches)} searches")
        return plan

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        logger.info(f"Performing {len(search_plan.searches)} searches")
        with custom_span("Search the web"):
            tasks = [
                asyncio.create_task(self._search(item)) for item in search_plan.searches
            ]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)

            logger.info(f"Completed {len(results)} searches successfully")
            return results

    async def _search(self, item: WebSearchItem) -> str | None:
        logger.info(f"Searching for: {item.query}")
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            logger.info(f"Search completed for: {item.query}")
            return str(result.final_output)
        except Exception as e:
            logger.error(f"Search failed for: {item.query}. Error: {e}", exc_info=True)
            return None

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        logger.info("Writing report")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        logger.info("Report writing completed")
        return result.final_output_as(ReportData)

    async def _generate_chart(self, chart_request: ChartRequest) -> str:
        """Generate a chart and return the chart URL or base64 image"""
        logger.info(f"Generating chart: {chart_request.title}")
        with custom_span("Generate chart"):
            try:
                chart_url = generate_chart(chart_request)
                logger.info(f"Chart generated successfully: {chart_request.title}")
                return chart_url
            except Exception as e:
                logger.error(f"Error generating chart: {e}", exc_info=True)
                return None
