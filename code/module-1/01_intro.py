from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama

load_dotenv()

messages = []

model = ChatOllama(model="qwen2.5:3b", temperature=1.0)
agent = create_agent(
    model=model,
    system_prompt="You are a science fiction writer, respond in a creative way."
)

input_prompt = input("> ")
while input_prompt != '/bye':
    messages.append(HumanMessage(content=input_prompt))
    response = agent.invoke(
        {"messages": messages}
    )
    messages = response['messages']
    print(f"[AI]: {response['messages'][-1].content}")
    input_prompt = input("> ")