from dotenv import load_dotenv
from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse, dynamic_prompt
from langchain.chat_models import init_chat_model
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv()


@dataclass
class SelectAgent:
    agent: str = "normal"


agent_prompts = {
    "normal": "You are a math tutor. You provide detail explanation on mathematics concept.",
    "haiku": "Your response must only be in haiku."
}

@dynamic_prompt
def select_agent(request: ModelRequest) -> str:
    """Select agent dynamically"""

    agent_choice = request.runtime.context.agent
    prompt = agent_prompts[agent_choice]
    return prompt


agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    context_schema=SelectAgent,
    middleware=[select_agent]
)

response = agent.invoke(
    {"messages": [HumanMessage(content="What is trignometry?")]},
    context=SelectAgent()
)
print("Response: ", response["messages"][-1].content[-1]['text'])

print("-"*25)
response = agent.invoke(
    {"messages": [HumanMessage(content="What is trignometry?")]},
    context=SelectAgent(agent="haiku")
)
print("Response: ", response["messages"][-1].content[-1]['text'])

print("-"*25)
response = agent.invoke(
    {"messages": [HumanMessage(content="What is algebra?")]},
    context=SelectAgent(agent="haiku")
)
print("Response: ", response["messages"][-1].content[-1]['text'])
