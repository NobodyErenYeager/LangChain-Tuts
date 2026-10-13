from dotenv import load_dotenv
from collections.abc import Callable

from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain.chat_models import init_chat_model
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.messages import HumanMessage

@dataclass
class ModelChoice:
    model: str = "b"

load_dotenv()

models = {
    "a": "google_genai:gemini-3.5-flash-lite",
    "b": "google_genai:gemini-3.1-flash-lite"
}


@wrap_model_call
def switch_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Switch Model based on user choice"""

    model_choice = request.runtime.context.model
    selected_model = models.get(model_choice, None)
    if selected_model:
        request = request.override(
            model=init_chat_model(selected_model)
        )

    return handler(request)


agent = create_agent(
    model=models["b"],
    middleware=[switch_model],
    system_prompt="You are roleplaying a real life helpful office intern.",
    context_schema=ModelChoice
)

response = agent.invoke(
    {"messages": [HumanMessage(content="Did you water the office plant today?")]},
    context=ModelChoice()
)

print("Response: ", response["messages"][-1].content[-1]['text'])
print("Model: ", response["messages"][-1].response_metadata["model_name"])


response = agent.invoke(
    {"messages": [HumanMessage(content="When should we expect to have to replace the pot?")]},
    context=ModelChoice(model='a')
)

print("Response: ", response["messages"][-1].content[-1]['text'])
print("Model: ", response["messages"][-1].response_metadata["model_name"])
