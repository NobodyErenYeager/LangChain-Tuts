from dataclasses import dataclass

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import ToolRuntime, tool

load_dotenv()


@dataclass
class UserInfo:
    username: str = "John Doe"
    mobile_no: str = "9876543210"
    role: str = "admin"


@tool
def get_user_info(runtime: ToolRuntime[UserInfo]) -> str:
    """Get user info"""
    context = runtime.context
    return f"Username: {context.username}, Mobile No.: {context.mobile_no}, Role: {context.role}"


agent = create_agent(
    model='google_genai:gemini-3.1-flash-lite',
    tools=[get_user_info],
    context_schema=UserInfo
)

response = agent.invoke(
    {"messages": [HumanMessage(content="Show me my profile.")]},
    context=UserInfo()
)

print(response['messages'][-1].content[-1]['text'])
