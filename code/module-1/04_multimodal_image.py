import base64
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# https://medium.com/@dimosdennis/personal-photo-library-with-langchain-ollama-llava-fully-local-e82edfe07f54
# for ollama

load_dotenv()

image_path = Path(r"<image_path>")
image_base64 = base64.b64encode(
    image_path.read_bytes()
).decode("utf-8")

agent = create_agent(model="google_genai:gemini-3.1-flash-lite")

multimodal_question = HumanMessage(content=[
    {"type": "text", "text": "Tell me about this image."},
    {"type": "image", "base64": image_base64, "mime_type": "image/png"}
])

result = agent.invoke(
    {"messages": [multimodal_question]}
)

print(result['messages'][-1].content[-1]['text'])