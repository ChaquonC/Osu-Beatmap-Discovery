from enum import Enum


class LLMActionTypes(Enum):
    RESPOND = "Give final response"
    QUESTION = "Ask clarifying question"
    TOOL = "make tool call"

async def call_agent(prompt: str):
