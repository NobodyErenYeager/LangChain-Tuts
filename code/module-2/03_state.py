from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

load_dotenv()

class Table(AgentState):
    fields: list[str]


@tool
def update_fields_state(fields: list[str], runtime: ToolRuntime):
    """Update the fields for the table once the table is created"""

    return Command(update={
        "fields": fields,
        "messages": [ToolMessage("Successfully updated the fields", tool_call_id=runtime.tool_call_id)]
    })

config = {"configurable": {"thread_id": str(uuid4())}}
print(config)

agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[update_fields_state],
    checkpointer=InMemorySaver(),
    state_schema=Table,
    system_prompt="You are a sql expert. You create query based on the users input"
)

response = agent.invoke(
    {"messages": [HumanMessage("Create a query for todo list table with fields task, completed, created on and completed on")]},
    config
)

print(response['fields'])

for message in response['messages']:
    print(message)
    print("-"*25)