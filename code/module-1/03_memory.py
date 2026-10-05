from uuid import uuid4

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

config = {'configurable': {'thread_id': str(uuid4())}}

agent = create_agent(
    model="ollama:qwen2.5:3b",
    checkpointer=InMemorySaver()
)

input_prompt = input("> ")
while input_prompt != '/bye':
    response = agent.invoke(
        {"messages": [HumanMessage(content=input_prompt)]},
        config
    )
    print(f"[AI]: {response['messages'][-1].content}\n\n")
    input_prompt = input("> ")