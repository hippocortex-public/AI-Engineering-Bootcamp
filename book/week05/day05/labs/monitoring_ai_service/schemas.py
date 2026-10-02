from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    user_id: str | None = None


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float


class HealthResponse(BaseModel):
    status: str
    service: str
    checks: dict[str, str]
