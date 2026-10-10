from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool

load_dotenv()

tamil_agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    system_prompt="You are a tamil agent. You reply only in tamil"
)

spanish_agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    system_prompt="You are a spanish agent. You reply only in spanish"
)


@tool
def call_tamil_agent(query: str) -> str:
    """Call Tamil Agent when you need to translate to tamil"""
    response = tamil_agent.invoke({"messages": [HumanMessage(query)]})
    return response['messages'][-1].content[-1]['text']


@tool
def call_spanish_agent(query: str) -> str:
    """Call Spanish Agent when you need to translate to spanish"""
    response = spanish_agent.invoke({"messages": [HumanMessage(query)]})
    return response['messages'][-1].content[-1]['text']


language_coordinator = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    system_prompt="You are a language coordinator. You have two subagents for translating to tamil and spanish. Do not translate to other language when user asks.",
    tools=[call_tamil_agent, call_spanish_agent]
)

response = language_coordinator.invoke({'messages': [HumanMessage("Translate this to tamil: How are you?")]})
print(response['messages'][-1].content[-1]['text'])
response = language_coordinator.invoke({'messages': [HumanMessage("Translate this to spanish: How are you?")]})
print(response['messages'][-1].content[-1]['text'])
response = language_coordinator.invoke({'messages': [HumanMessage("Translate this to hindi: How are you?")]})
print(response['messages'][-1].content[-1]['text'])
