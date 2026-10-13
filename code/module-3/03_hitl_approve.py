from dotenv import load_dotenv
from langchain.tools import ToolRuntime, tool
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4
from langgraph.types import Command
from pprint import pprint

load_dotenv()

class EmailState(AgentState):
    email: str


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

agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    tools=[read_email, send_email],
    state_schema=EmailState,
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,
                "send_email": True,
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)
config = {"configurable": {"thread_id": str(uuid4())}}

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Please read my email and send a response immediately. Send the reply now in the same thread.")],
        "email": "Hi Seán, I'm going to be late for our meeting tomorrow. Can we reschedule? Best, John."
    },
    config=config
)
print(response['__interrupt__'][0].value['action_requests'][0]['args']['body'])
response = agent.invoke(
    Command( 
        resume={"decisions": [{"type": "approve"}]}
    ), 
    config=config
)

pprint(response)