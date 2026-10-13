from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from pprint import pprint
from langchain.messages import AIMessage, HumanMessage
from uuid import uuid4

load_dotenv()

agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="google_genai:gemini-3.1-flash-lite",
            trigger=("tokens", 100),
            keep=("messages", 1)
        )
    ],
)

response = agent.invoke(
    {"messages": [
        HumanMessage(content="What is the capital of the moon?"),
        AIMessage(content="The capital of the moon is Lunapolis."),
        HumanMessage(content="What is the weather in Lunapolis?"),
        AIMessage(content="Skies are clear, with a high of 120C and a low of -100C."),
        HumanMessage(content="How many cheese miners live in Lunapolis?"),
        AIMessage(content="There are 100,000 cheese miners living in Lunapolis."),
        HumanMessage(content="Do you think the cheese miners' union will strike?"),
        AIMessage(content="Yes, because they are unhappy with the new president."),
        HumanMessage(content="If you were Lunapolis' new president how would you respond to the cheese miners' union?"),
        ]},
    {"configurable": {"thread_id": str(uuid4())}}
)

pprint(response)