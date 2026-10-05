import base64
from typing import Annotated, Any
from uuid import UUID, uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from tavily.client import TavilyClient

load_dotenv()

app = FastAPI()

SUPPORTED_AUDIO_FORMATS = ["audio/mpeg", "audio/wav"]
SUPPORTED_VIDEO_FORMATS = ["video/mp4", "video/webm"]
SUPPORTED_IMAGE_FORMATS = ["image/jpeg", "image/png"]
SUPPORTED_TEXT_FORMATS = ["text/plain", "text/csv", "text/html", "text/css", "text/markdown", 
                          "text/javascript", "application/xml", "application/json"]
SUPPORTED_DOCUMENT_FORMATS = ['application/pdf'] + SUPPORTED_TEXT_FORMATS

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> dict[str, Any]:
    """Search the web for information."""
    try:
        return tavily_client.search(query)
    except Exception:
        return {"error": "Unable to search the web"}


def convert_to_b64(content):
    return base64.b64encode(content).decode("utf-8")


def get_file_data(file: UploadFile, content):
    file_data = {
        "type": None,
        "base64": convert_to_b64(content),
        "mime_type": file.content_type

    }
    if file.content_type in SUPPORTED_IMAGE_FORMATS:
        file_data["type"] = "image"
        return file_data
    elif file.content_type in SUPPORTED_AUDIO_FORMATS:
        file_data["type"] = "audio"
        return file_data
    elif file.content_type in SUPPORTED_VIDEO_FORMATS:
        file_data["type"] = "video"
        return file_data
    elif file.content_type in SUPPORTED_DOCUMENT_FORMATS:
        file_data["type"] = "file"
        return file_data
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")


agent = create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    tools=[web_search],
    system_prompt="You are a personal assistant.",
    checkpointer=InMemorySaver()
)


@app.post('/')
async def chat(
    id: Annotated[UUID, Form(default_factory=uuid4)],
    prompt: Annotated[str, Form()],
    file: Annotated[UploadFile | None, File()] = None
):
    config = {'configurable': {'thread_id': str(id)}}
    messages = [{"type": "text", "text": prompt}]
    file_data = {}
    if file:
        print(file.content_type)
        contents = await file.read()
        file_data = get_file_data(file, contents)
        messages.append(file_data)

    response = agent.invoke(
        {"messages": [HumanMessage(content=messages)]},
        config=config
    )

    ai_message = response['messages'][-1].content[-1]['text']

    return {
        "id": id,
        "ai_message": ai_message
    }