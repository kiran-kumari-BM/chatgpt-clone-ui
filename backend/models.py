from typing import List, Optional
from pydantic import BaseModel


class UploadedFileInfo(BaseModel):
    filename: str
    content_type: str
    size: int


class ChatRequest(BaseModel):
    prompt: str
    conversation_id: Optional[str] = None
    files: List[UploadedFileInfo] = []


class ChatResponse(BaseModel):
    answer: str
