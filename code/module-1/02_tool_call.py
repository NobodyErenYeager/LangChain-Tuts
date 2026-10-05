from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from tavily.client import TavilyClient

load_dotenv()
tavily_client = TavilyClient()


@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information."""
    try:
        return tavily_client.search(query)
    except Exception:
        return {"error": "Unable to search the web"}


agent = create_agent(
    model="ollama:qwen2.5:3b",
    tools=[web_search],
    system_prompt="You are a personal assistant."
)

response = agent.invoke(
    {"messages": [HumanMessage(content="How up to date is your training knowledge?")]}
)
print(response['messages'][-1].content)

response = agent.invoke(
    {"messages": [HumanMessage(content="Who is the current cheif minister of Tamil Nadu?")]}
)
print(response['messages'][-1].content)
