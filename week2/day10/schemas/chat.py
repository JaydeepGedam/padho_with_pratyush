
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000
    )
    session_id: str = Field(min_length=1, max_length=100)


class ChatResponse(BaseModel):
    answer: str

class ClearChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
