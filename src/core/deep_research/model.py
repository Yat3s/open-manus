from openai import AsyncOpenAI
from pydantic import BaseModel

from ..config import Config
from agents import OpenAIChatCompletionsModel

# 创建外部API客户端
external_client = AsyncOpenAI(
    base_url=Config.EXTERNAL_API_BASE_URL,
    api_key=Config.EXTERNAL_API_KEY,
)

class PlannerModel:
    MODEL_NAME = "o3-mini"
    DESCRIPTION = "用于投资研究报告规划的高级模型"
    
    @classmethod
    def get_model(cls):
        return OpenAIChatCompletionsModel(
            model=cls.MODEL_NAME, 
            openai_client=external_client
        )

class ResearchModel:
    MODEL_NAME = "gpt-4o"
    DESCRIPTION = "用于信息搜索和数据收集的模型"
    
    @classmethod
    def get_model(cls):
        return cls.MODEL_NAME
    
    @staticmethod
    def get_model_settings():
        from agents.model_settings import ModelSettings
        return ModelSettings(tool_choice="required")

class ComposeModel:
    MODEL_NAME = "o3-mini" 
    DESCRIPTION = "用于综合研究结果并生成最终报告的模型"
    
    @classmethod
    def get_model(cls):
        return OpenAIChatCompletionsModel(
            model=cls.MODEL_NAME, 
            openai_client=external_client
        )

