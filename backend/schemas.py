from pydantic import BaseModel
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    body: str | None = None

class NoteResponse(NoteCreate):
    id: int
    created_at: datetime
    edited_at: datetime
    tags: list[TagResponse] = []

class TagResponse(BaseModel):
    id: int
    name: str
