import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

async def get_agent():
    mcp_clients = MultiServerMCPClient({
        "docs-langchain": {
            "transport": "streamable_http",
            "url": "https://docs.langchain.com/mcp"
        },
        "reference-langchain": {
            "transport": "streamable_http",
            "url": "https://reference.langchain.com/mcp"
        }
    })
    tools = await mcp_clients.get_tools()

    return create_agent(
        model="google_genai:gemini-3.1-flash-lite",
        tools=tools,
        system_prompt="You are an expert in Langchain. You have the tools for langchain documents and references"
    )

async def main():
    agent = await get_agent()
    prompt = input("Enter the input prompt: ")
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=prompt)]}
    )

    for block in result['messages'][-1].content_blocks:
        if block['type'] == "text":
            print(block['text'])

asyncio.run(main())


"""
filesystem = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(workspace)],
            cwd=str(workspace),  # start the server in the workspace so relative file names resolve there
        ),
        timeout=60
    ),
    errlog=subprocess.DEVNULL,
)
"""