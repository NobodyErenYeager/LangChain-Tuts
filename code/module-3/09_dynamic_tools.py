from dotenv import load_dotenv
from collections.abc import Callable
import asyncio

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
from langchain.agents import create_agent, AgentState
from langchain.messages import HumanMessage

load_dotenv()

class EmailState(AgentState):
    email: str

@dataclass
class Subscription:
    tier: str = "free"

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the given address."""
    # take email from state
    return runtime.state["email"]


@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    # fake email sending
    print(body)
    return "Email sent"

@wrap_model_call
async def set_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """Get tools dynamically"""

    subscription = request.runtime.context.tier

    tools = []
    if subscription == "basic":
        tools = [read_email]
    elif subscription == "pro":
        tools = [read_email, send_email]

    print(
        f"Tier: {subscription}, "
        f"Available tools: {[tool.name for tool in tools]}"
    )
    
    request = request.override(tools=tools)

    return await handler(request)


agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    tools=[read_email, send_email],
    middleware=[set_tools],
    context_schema=Subscription,
    state_schema=EmailState
)

async def run():
    response = await agent.ainvoke(
        {
            "messages": [HumanMessage(content="Can you check my inbox?")],
            "email": "No new mail in inbox"
        },
        context=Subscription()
    )
    print("Response: ", response["messages"][-1].content[-1]['text'])

    print("-"*25)
    response = await agent.ainvoke(
        {
            "messages": [HumanMessage(content="Can you check my inbox?")],
            "email": "No new mail in inbox"
        },
        context=Subscription(tier="basic")
    )
    print("Response: ", response["messages"][-1].content[-1]['text'])

    print("-"*25)
    response = await agent.ainvoke(
        {
            "messages": [HumanMessage(content="Can you send an email to someone@anymail.com that i'll be late for the meeting.")],
            "email": "No new mail in inbox"
        },
        context=Subscription(tier="basic")
    )
    print("Response: ", response["messages"][-1].content[-1]['text'])

    print("-"*25)
    response = await agent.ainvoke(
        {
            "messages": [HumanMessage(content="Can you send an email to someone@anymail.com that i'll be late for the meeting.")],
            "email": "No new mail in inbox"
        },
        context=Subscription(tier="pro")
    )
    print("Response: ", response["messages"][-1].content[-1]['text'])


asyncio.run(run())