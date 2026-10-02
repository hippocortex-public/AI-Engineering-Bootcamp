from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ChatRequest(StrictPayload):
    message: str = Field(min_length=1, max_length=2000)
    document_id: str | None = Field(default=None, pattern=r"^[a-z0-9_-]{1,64}$")

    @field_validator("message")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Blank message")
        return value


class ToolRequest(StrictPayload):
    name: str = Field(min_length=1, max_length=64)
    arguments: dict


class ReadDocumentArguments(StrictPayload):
    document_id: str = Field(pattern=r"^[a-z0-9_-]{1,64}$")
