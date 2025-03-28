from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from agents import (
    Agent,
    RunContextWrapper,
    function_tool,
)
from browser_use import Agent as BrowserAgent, Browser

INSTRUCTIONS = """
    You are a browser agent. Your goal is to fetch detailed information based on the user's query.
    # Process:
    1. Use the `browser_search` tool to get information about the user's query.
    2. Save the retrieved information in the context.
    3. Present the information in a structured format to the user.
"""


class BrowserSearchContext(BaseModel):
    query: str = Field(default="", description="The search query provided by the user")
    searchResults: str = Field(
        default="", description="Raw data retrieved from the browser search"
    )


@function_tool(
    name_override="browser_search",
    description_override="Searches online for information based on the user's query.",
)
async def browser_search(
    context: RunContextWrapper[BrowserSearchContext], query: str
) -> str:
    llm = ChatOpenAI(model="gpt-4o")
    agent = BrowserAgent(
        task=f"Find detailed information about {query} and return structured data.",
        llm=llm,
        browser=Browser(),
    )
    history = await agent.run()

    ## update the context with the extracted content
    context.context.searchResults = history.extracted_content()
    print("updated context - ", context.context)
    return history.extracted_content()


browser_agent = Agent[BrowserSearchContext](
    name="Browser Agent",
    handoff_description="An agent that searches for information online.",
    instructions=INSTRUCTIONS,
    tools=[browser_search],
)
