from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    conversation_id: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
    model: str = "demo-llm"
    prompt_version: str = "v1"


class ChatResponse(BaseModel):
    source: str
    answer: str
    cache_key: str
