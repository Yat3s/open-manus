from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from browser_use import Agent as BrowserAgent, Controller


class BrowserResult(BaseModel):
    content: list[str]


class BrowserTool:
    def __init__(self):
        self.controller = Controller(output_model=BrowserResult)
        self.model = ChatOpenAI(model="gpt-4o")

    async def browse(self, task: str) -> list[str]:
        """Use the browser tool to execute a task and return a list of string results"""
        agent = BrowserAgent(task=task, llm=self.model)

        history = await agent.run()
        result = history.final_result()
        print("Search result:")
        print(result)

        if result:
            validated_result = BrowserResult.model_validate_json(result)
            return validated_result.content
        return []
