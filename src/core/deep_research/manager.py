from __future__ import annotations

import asyncio

from rich.console import Console

from agents import Runner, custom_span, gen_trace_id, trace

from .agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from .agents.search_agent import search_agent
from .agents.writer_agent import ReportData, writer_agent
from .printer import Printer


class DeepResearchManager:
    def __init__(self):
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, query: str) -> dict:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            report = await self._write_report(query, search_results)
            print(report.image_requests)

            processed_report = report.markdown_report
            for i, img_request in enumerate(report.image_requests):
                image_url = await self._generate_image(img_request.search_query)
                markdown_image = f"\n![{img_request.caption}]({image_url})\n"
                placeholder = f"{{{{{img_request.position}}}}}"
                processed_report = processed_report.replace(placeholder, markdown_image)

            return {
                "trace_id": trace_id,
                "report": processed_report,
                "summary": report.short_summary,
                "follow_up_questions": report.follow_up_questions,
            }

    async def _plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        with custom_span("Search the web"):
            tasks = [
                asyncio.create_task(self._search(item)) for item in search_plan.searches
            ]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
            return results

    async def _search(self, item: WebSearchItem) -> str | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(
            writer_agent,
            input,
        )

        async for _ in result.stream_events():
            pass

        return result.final_output_as(ReportData)

    async def _generate_image(self, search_query: str) -> str:
        # TODO: Generate image from search query
        return "https://xmodel.blob.core.windows.net/predictions/output/6258ce40-7260-4662-8e9e-8d9dde4cfbba.png"
