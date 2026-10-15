from schemas import EmailSchema, AgentSchema, ChatSchema, ChatResponseSchema, ActionResponse, ActionType
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.tools import ToolRuntime, tool
from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from uuid import uuid4
from langgraph.types import Command
from dataclasses import dataclass
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call, dynamic_prompt
from typing import Callable
from langchain.chat_models import init_chat_model

load_dotenv()

app = FastAPI()

emails = []

available_agents = {
    "personal_assistant": AgentSchema(
        name="personal_assistant",
        system_prompt="You are a personal assistant."
    )
}

models = {
    "a": "google_genai:gemini-3.5-flash-lite",
    "b": "google_genai:gemini-3.1-flash-lite"
}


@dataclass
class AgentContext:
    model: str = "b"
    agent: str = "personal_assistant"
    subscription: str = "free"


@tool
def get_unread_emails() -> list[str]:
    """Get Unread emails from Inbox"""
    unread = [email.email for email in emails if email.read == False]
    return unread


@tool
def send_email(body: str) -> str:
    """Send an email to the given address with the given subject and body."""
    print("[Sending Email]: ", body)
    return "Email Sent"


@wrap_model_call
def select_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Select model based on User request"""
    selected = request.runtime.context.model
    if model_choice := models.get(selected, None):
        request = request.override(
            model=init_chat_model(model_choice)
        )

    return handler(request)


@wrap_model_call
def set_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Set tools based on Users subscription"""
    subscription = request.runtime.context.subscription

    if subscription == "pro":
        tools = request.tools
    elif subscription == "basic":
        tools = [get_unread_emails]
    else:
        tools = []

    request = request.override(tools=tools)
    return handler(request)


@dynamic_prompt
def change_prompt(request: ModelRequest) -> str:
    """Change prompt based on user request"""
    agent_choice = request.runtime.context.agent
    prompt = available_agents.get(agent_choice, "personal_assistant").system_prompt
    return prompt


agent = create_agent(
    model=models["b"],
    system_prompt=available_agents['personal_assistant'].system_prompt,
    tools=[get_unread_emails, send_email],
    checkpointer=InMemorySaver(),
    context_schema=AgentContext,
    middleware=[
        set_tools,
        select_model,
        change_prompt,
        HumanInTheLoopMiddleware(
            interrupt_on={
                "get_unread_emails": False,
                "send_email": True
            },
            description_prefix="Tool execution requires approval"
        )
    ]
)


def get_text(message):
    return "".join(
        block["text"]
        for block in message.content_blocks
        if block["type"] == "text"
    )


@app.post('/email')
def create_email(email: EmailSchema):
    emails.append(email)
    return email


@app.get('/email/list')
def create_email():
    return emails


@app.get('/agents')
def get_agents():
    return available_agents


@app.post('/agents')
def create_agents(agent_schema: AgentSchema):
    available_agents[agent_schema.name] = agent_schema
    return available_agents


@app.post('/chat')
def chat(prompt: ChatSchema | ActionResponse) -> ChatResponseSchema:
    print("Chat: ", isinstance(prompt, ChatSchema))
    print("Action: ", isinstance(prompt, ActionResponse))
    config = {"configurable": {"thread_id": str(prompt.id)}}
    agent_context = {
        "model": prompt.model,
        "agent": prompt.agent,
        "subscription": prompt.subscription.value
    }

    if isinstance(prompt, ChatSchema):
        response = agent.invoke(
            {"messages": [HumanMessage(prompt.prompt)]},
            config=config,
            context=agent_context
        )
    elif isinstance(prompt, ActionResponse):
        decisions = {"type": prompt.action_type.value}
        if prompt.action_type == ActionType.reject:
            decisions['message'] = prompt.message
        elif prompt.action_type == ActionType.edit:
            decisions['edited_action'] = {
                "name": "send_email",
                "args": {"body": prompt.message},
            }
        response = agent.invoke(
            Command(resume={"decisions": [decisions]}), 
            config=config,
            context=agent_context,
        )
    # print(response)

    chat_response = ChatResponseSchema(
        id=prompt.id,
        ai_message="",
        model=response['messages'][-1].response_metadata["model_name"],
        agent=prompt.agent
    )
    if interupt := response.get("__interrupt__", None):
        # print(interupt)
        details = interupt[0].value['action_requests'][0]
        chat_response.ai_message = details['description']
        chat_response.interupt_action = details
        # print(chat_response.model_dump_json)
    else:
        chat_response.ai_message = get_text(response['messages'][-1])
    return chat_response
