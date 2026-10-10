import asyncio
import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from prompts import (
    BACKEND_AGENT,
    DOCUMENTATION_AGENT,
    FRONTEND_AGENT,
    PROJECT_COORDINATOR_AGENT,
)

load_dotenv()
CONTEXT7_API_KEY = os.getenv('CONTEXT7_API_KEY')
MODEL = "google_genai:gemini-3.6-flash"

@tool
def update_state(runtime: ToolRuntime, application_request:str="", base_url:str="", port:str="", python_file_path:str="", document_file_path:str=""):
    """Update the state when you know any of the values: application_request, base_url, port, python_file_path, document_file_path.
This tool must be called alone, without any other tool calls. It must complete and return to make,
the information available to other tools."""
    print("-"*10)
    print("[CALLED] State Update Tool.")
    print(f"\tapplication_request: {application_request}")
    print(f"\tbase_url: {base_url}")
    print(f"\tport: {port}")
    print(f"\tpython_file_path: {python_file_path}")
    print(f"\tdocument_file_path: {document_file_path}")
    print("-"*10)
    return Command(update={
        "application_request": application_request,
        "base_url": base_url,
        "port": port,
        "python_file_path": python_file_path,
        "document_file_path": document_file_path,
        "messages": [ToolMessage("Successfully updated the state", tool_call_id=runtime.tool_call_id)]
    })


def get_text(message):
    return "".join(
        block["text"]
        for block in message.content_blocks
        if block["type"] == "text"
    )


class SubAgent:
    model = None
    agent = None
    prompt = None

    def __init__(self, prompt: str, model: str="ollama:gemma4:e2b"):
        self.prompt = prompt
        self.model = model

    async def start(self, tools):
        self.agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt=self.prompt
        )

    async def run(self, query):
        response = await self.agent.ainvoke({"messages": [HumanMessage(query)]})
        return get_text(response['messages'][-1])


backend_agent = SubAgent(BACKEND_AGENT, MODEL)
documentation_agent = SubAgent(DOCUMENTATION_AGENT, MODEL)
frontend_agent = SubAgent(FRONTEND_AGENT, MODEL)

@tool
async def call_backend_agent(query: str):
    """Call backend agent for backend related works."""
    print("[STARTED] Backend Agent.")
    response = await backend_agent.run(query)
    print("[COMPLETED] Backend Agent.")
    return response

@tool
async def call_documentation_agent(query: str):
    """Call documentation agent for documentation related works."""
    print("[STARTED] Documentation Agent.")
    response = await documentation_agent.run(query)
    print("[COMPLETED] Documentation Agent.")
    return response

@tool
async def call_frontend_agent(query: str):
    """Call frontend agent for frontend related works."""
    print("[STARTED] Frontend Agent.")
    response = await frontend_agent.run(query)
    print("[COMPLETED] Frontend Agent.")
    return response


class ProjectState(AgentState):
    application_request: str
    base_url: str
    port: str
    python_file_path: str
    document_file_path: str


class ProjectCoordinator:
    model = None
    agent = None

    def __init__(self, model: str="ollama:gemma4:e2b"):
        self.model = model

    async def get_sub_agents_mcps(self):
        work_dir = Path('sandbox/todo_list').resolve()
        client = MultiServerMCPClient({
            "local_server": {
                "transport": "stdio",
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(work_dir)],
            },
            "context7": {
                "transport": "streamable_http",
                "url": "https://mcp.context7.com/mcp",
                "headers": {
                    "Authorization": f"Bearer {CONTEXT7_API_KEY}"
                }
            }
        })

        tools = await client.get_tools()
        return tools

    async def create_subagents(self):
        print("[STARTED] Creating Sub Agents MCPs.")
        sub_agents_tools = await self.get_sub_agents_mcps()
        print("[COMPLETED] Creating Sub Agents MCPs.")

        await backend_agent.start(sub_agents_tools)
        await documentation_agent.start(sub_agents_tools)
        await frontend_agent.start(sub_agents_tools)

    async def start(self):
        print("[STARTED] Creating Sub Agents.")
        await self.create_subagents()
        print("[COMPLETED] Creating Sub Agents.")

        print("[STARTED] Creating Main Agent.")
        self.agent = create_agent(
            model=self.model,
            tools=[update_state, call_backend_agent, call_documentation_agent, call_frontend_agent],
            checkpointer=InMemorySaver(),
            state_schema=ProjectState,
            system_prompt=PROJECT_COORDINATOR_AGENT
        )
        print("[COMPLETED] Creating Main Agent.")

    async def run(self, input_prompt:str, thread_id:str="test"):
        print("[STARTED] Project Coordinator Agent.")
        config = {'configurable': {'thread_id': str(thread_id)}}
        response = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=input_prompt)]},
            config
        )
        print("[COMPLETED] Project Coordinator Agent.")

        return response


if __name__ == "__main__":
    prompt = """Create a simple todo app.
Use fastapi as the backend and use json to store the data.
The backend code must only be in single file.
For frontend use react."""
    id = str(uuid4())
    async def main():
        project_coordinator = ProjectCoordinator(MODEL)
        await project_coordinator.start()
        response = await project_coordinator.run(prompt, thread_id=id)
        print(response)

    asyncio.run(main())
    