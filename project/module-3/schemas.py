from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum

class ActionType(str, Enum):
    approve = "approve"
    reject = "reject"
    edit = "edit"


class MessageType(str, Enum):
    normal = "normal"
    hitl = "hitl"


class Subscription(str, Enum):
    free = "free"
    basic = "basic"
    pro = "pro"


class EmailSchema(BaseModel):
    email: str
    read: bool = False


class AgentSchema(BaseModel):
    name: str
    system_prompt: str


class Chat(BaseModel):
    id: UUID = uuid4()
    model: str = "b"
    agent: str = "personal_assistant"
    subscription: Subscription = Subscription.free


class ChatSchema(Chat):
    prompt: str


class InteruptAction(BaseModel):
    name: str|None = None
    args: dict|None = None


class ChatResponseSchema(BaseModel):
    id: UUID
    model: str
    agent: str
    ai_message: str
    interupt_action: InteruptAction|None = None
    message_type: MessageType = MessageType.normal


class ActionResponse(Chat):
    action_type: ActionType
    message: str|None = None
