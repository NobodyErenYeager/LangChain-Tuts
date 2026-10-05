import base64
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv()

audio_path = Path(r"<audio_path>")
audio_base64 = base64.b64encode(
    audio_path.read_bytes()
).decode("utf-8")

agent = create_agent(model="google_genai:gemini-3.1-flash-lite")

multimodal_question = HumanMessage(content=[
    {"type": "text", "text": "Transcribe this audio."},
    {"type": "audio", "base64": audio_base64, "mime_type": "audio/mp3"}
])

result = agent.invoke(
    {"messages": [multimodal_question]}
)

print(result['messages'][-1].content[-1]['text'])