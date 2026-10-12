from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The customer's message")
    history: list[ChatMessage] = Field(
        default_factory=list,
        description="Prior turns in this conversation, oldest first",
    )


class ChatResponse(BaseModel):
    reply: str